
from cmath import e
import collections
import dataclasses
import textwrap
import sqlite3
import databases
import toml
import random

from quart import Quart, g, request, abort
# from quart_auth import basic_auth_required

from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

app = Quart(__name__)
QuartSchema(app)

app.config.from_file(f"./etc/{__name__}.toml", toml.load)


@dataclasses.dataclass
class user:
    username: str
    userpassword: str


@dataclasses.dataclass
class guess:
    game_id: int
    guess_word: str


async def _get_db():
    db = getattr(g, "_sqlite_db", None)
    if db is None:
        db = g._sqlite_db = databases.Database(app.config["DATABASES"]["URL"])
        await db.connect()
    return db


@app.teardown_appcontext
async def close_connection(exception):
    db = getattr(g, "_sqlite_db", None)
    if db is not None:
        await db.disconnect()


@app.route("/")
def index():
    return textwrap.dedent(
        """
        <h1>Welcome to the Wordle</h1>

        """
    )

# Start of User API
@app.route("/user/registeration", methods=["POST"])
@validate_request(user)
async def register_user(data):
    db = await _get_db()
    user = dataclasses.asdict(data)
    try:
        id = await db.execute(
            """
            INSERT INTO User(username, password)
            VALUES(:username, :userpassword)
            """,
            user,
        )
    except sqlite3.IntegrityError as e:
        abort(409, e)

    user["user_id"] = id
    return user, 201, {"Location": f"/user/registeration/{id}"}


@app.errorhandler(RequestSchemaValidationError)
def bad_request(e):
    return {"error": str(e.validation_error)}, 400


@app.errorhandler(409)
def conflict(e):
    return {"error": str(e)}, 409


# user authentication from db
async def authenticate_user(username, password):
    db = await _get_db()
    user = await db.fetch_one("SELECT * FROM User WHERE username =:username AND password =:password", values={"username": username, "password": password})

    return user

# authentication API
@app.route("/authentication")
async def authentication():
    if not request.authorization:
        return {"error": "Could not verify user"}, 401, {'WWW-Authenticate': 'Basic realm="MyApp"'}
    else:
        auth = request.authorization
        user = await authenticate_user(auth.username, auth.password)
        if user:
            return {"authenticated": "true"}, 200
        else:
            abort(401)


@app.errorhandler(401)
def not_found(e):
    return {"error": "Unauthorized"}, 401

# End of User API



# Start of Game API

# check if user_id present in db
async def validate_user_id(user_id):
    db = await _get_db()
    user_id = await db.fetch_one("SELECT * FROM User WHERE user_id =:user_id", values={"user_id": user_id})

    if user_id:
        return user_id
    else:
        abort(404, "User does not exist")


@app.errorhandler(404)
def not_found(e):
    return {"error": str(e)}, 404

# Check if game_id present in db 
async def validate_game_id(game_id):
    db = await _get_db()
    game_id = await db.fetch_one("SELECT game_id FROM Game WHERE game_id =:game_id ", values={"game_id": game_id})
    if game_id is None:
        abort(404, "game  does not exist")
    else:
         return game_id

# function to update In_progress table
async def update_inprogress(user_id, game_id):
    db = await _get_db()
    inprogressEntry = await db.execute("INSERT INTO In_Progress(user_id, game_id) VALUES (:user_id, :game_id)", values={"user_id": user_id, "game_id": game_id})
    if inprogressEntry:
        return inprogressEntry
    else:
        abort(417, "Failed to create entry in In_Progress table")


# New Game API
@app.route("/newgame/<int:user_id>", methods=["POST"])
async def newgame(user_id):
    userid = await validate_user_id(user_id)
    db = await _get_db()
    secret_word = await db.fetch_all("SELECT correct_word FROM Correct_Words")
    secret_word = random.choice(secret_word)
    game_id = await db.execute("INSERT INTO Game(user_id, secretword) VALUES (:user_id, :secretword)", values={"user_id": userid[0], "secretword": secret_word[0]})
    if game_id:
        inprogressEntry = await update_inprogress(userid[0], game_id)
        if inprogressEntry:
            return {"success": f"Your new game id is {game_id}"}, 201
        else:
            abort(417, "Failed to create entry in In_Progress table")

    else:
         abort(417, "New game creation failed")


@app.errorhandler(417)
def not_found(e):
    return {"error": str(e)}, 417


# Guess API
@app.route("/guess", methods=["POST"])
@validate_request(guess)
async def guess(data):
    db = await _get_db()
    payload = dataclasses.asdict(data)
    game_id = await validate_game_id(payload["game_id"])
    user_id = await db.fetch_one("SELECT user_id FROM Game WHERE game_id =:game_id ", values={"game_id": game_id[0]})

    if user_id[0] and game_id[0]:
        guessObject = {}
        in_progress = await db.fetch_all("SELECT * FROM In_Progress where game_id = " + str(payload["game_id"]))
        if (in_progress):
            secret_word = await db.fetch_one("SELECT secretword FROM Game where game_id = " + str(payload["game_id"]))
            secret_word = secret_word[0]

            is_valid_word_vj = await db.fetch_all('SELECT * FROM Valid_Words where valid_word = "' + str(payload["guess_word"]) + '";')
            is_valid_word_cj = await db.fetch_all('SELECT * FROM Correct_Words where correct_word = "' + str(payload["guess_word"]) + '";')

            guessEntry = await db.fetch_all("SELECT MAX(guess_num) FROM Guesses where game_id = " + str(payload["game_id"]))
            num = guessEntry[0][0]
            if len(is_valid_word_vj) or len(is_valid_word_cj):
                if (num):
                    guessObject["count"] = num + 1
                    if (num < 6):
                        temp = num + 1
                        game_id = await db.execute('INSERT INTO Guesses(game_id, guess_num, guess_word) VALUES (' + str(payload["game_id"]) + ', ' + str(temp) + ' , "' + str(payload["guess_word"])+'")')
                    else:
                        complete_game = await db.execute('INSERT INTO Completed(user_id, game_id , guess_num) VALUES (' + str(user_id[0]) + ', ' + str(payload["game_id"]) + ', ' + str(num) + ')')
                        game_over = await db.execute('DELETE FROM In_Progress where game_id = ' + str(payload["game_id"]))
                        return {"Message": "You Lose!! Start new game"}, 200
                else:
                    game_id = await db.execute('INSERT INTO Guesses(game_id, guess_num, guess_word) VALUES (' + str(payload["game_id"]) + ', 1 , "' + str(payload["guess_word"])+'")')
                    guessObject["count"] = 1
                if (game_id):
                    positionList = []

                    if (payload["guess_word"] == secret_word):
                        return {"Message": "Success, You guessed the right word."}, 200
                    else:
                        positionList = await guess_compute(payload["guess_word"], secret_word, positionList)
                        
                        guessObject["data"] = positionList
                        return guessObject, 201
                else:
                    abort(417)
            else:
                return {"error": "Not a Valid Word!"}, 404
        else:
            return {"message": "Game completed!!Start new game "}, 201
    else:
        abort(404, "resource does not exist")


# Game Status API
@app.route("/gamestaus/<int:game_id>", methods=["GET"])
async def game_status(game_id):
    db = await _get_db()
    secret_word1 = await db.fetch_one("SELECT secretword FROM Game where game_id = " + str(game_id))
    guesses_num = await db.fetch_all("SELECT max(guess_num) FROM Guesses WHERE game_id = " + str(game_id))
    guesses_word = await db.fetch_all("SELECT guess_word FROM Guesses WHERE game_id = " + str(game_id))
    num = guesses_num[0][0]
    gamestatus_object = []
    
    if num is None:
        abort(404,"No guesses available for this game_id")
    elif (num < 6):
        for i in range(num):

            guessObject = {}
            guessObject["guess"] = i+1
            positionList = []
            secret_word = secret_word1[0]      
            guess_word = guesses_word[i][0]

            positionList = await guess_compute(guess_word, secret_word, positionList)
            guessObject["guessword"] = positionList
            
            gamestatus_object.append(guessObject)
        return gamestatus_object,201
    
    else:
        return {"Message":"You have completed 6 guesses"}


# function to compute Guess API and Game status Logic
async def guess_compute(guess_word, secret_word,positionList):
    for j in guess_word:
        response = {}
        response[j] = "red"
        positionList.append(response)


    for i in range(5):
        if secret_word[i] in positionList[i].keys():
            positionList[i][list(positionList[i].keys())[0]] = "green"
            secret_word = secret_word[:i] + "_" + secret_word[i+1:]
                                

    for i,j in enumerate(guess_word):
        if j in secret_word and positionList[i][list(positionList[i].keys())[0]] != "green":
            positionList[i][list(positionList[i].keys())[0]] = "yellow"
            secret_word=secret_word.replace(j, "_")

    return positionList

# In progress game API
@app.route("/inprogressgame/<int:user_id>", methods=["GET"])
async def get_inprogressgame(user_id):
    userid = await validate_user_id(user_id)
    db = await _get_db()
    inprogressgames = await db.fetch_all("SELECT game_id FROM In_Progress WHERE user_id = :user_id", values={"user_id": userid[0]})
    if inprogressgames:
        if len(inprogressgames) >= 1:
            inprogressstring = str(inprogressgames[0][0])
            if len(inprogressgames) > 1:
                for i in range(1, len(inprogressgames)):
                    inprogressstring += ", " + str(inprogressgames[i][0])
                return {"message": f"Your in progress games are {inprogressstring}"}, 201
            return {"message": f"Your in progress game is {inprogressstring}"}, 201
    else:
        return {"message": f"There are no in progress games."}


