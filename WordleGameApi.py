
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
    # print("data******",  data)
    user = dataclasses.asdict(data)
    # print("user data***********",user)
    # print(user["username"])
    # print(user["userpassword"])

    try:
        id = await db.execute(
            """
            INSERT INTO user(username, userpassword)
            VALUES(:username, :userpassword)
            """,
            user,
        )
    except sqlite3.IntegrityError as e:
        abort(409, e)

    user["id"] = id
    return user, 201, {"Location": f"/user/registeration/{id}"}


@app.errorhandler(RequestSchemaValidationError)
def bad_request(e):
    return {"error": str(e.validation_error)}, 400


@app.errorhandler(409)
def conflict(e):
    return {"error": str(e)}, 409


async def authenticate_user(username,password):
    db = await _get_db()
    user = await db.fetch_one("SELECT * FROM user WHERE username =:username AND userpassword =:password", values={"username":username, "password":password})
    
    return user

@app.route("/login")
async def login():
    print("Request auth value" + str(request.authorization))
    print(not(request.authorization))
    if not request.authorization:
        return {"error":"Could not verify user"},401,{'WWW-Authenticate':'Basic realm="MyApp"'}
    else:
        auth = request.authorization
        user= await authenticate_user(auth.username, auth.password)
        if user:
            return {"authenticated": "true"},200
        else:
            abort(401)
    # return ""
        

@app.errorhandler(401)
def not_found(e):
    return {"error": "Unauthorized"}, 401




# End of User API
    
# Start of Game API

async def get_userid(username,password):
    db = await _get_db()
    userid = await db.fetch_one("SELECT userid FROM user WHERE username =:username AND userpassword =:password", values={"username":username, "password":password})
    print("in get user id" + str(userid))
    return userid



@app.route("/newgame" ,methods=["POST"])
async def newgame():
    auth = request.authorization
    print(auth)
    if auth:
        user= await authenticate_user(auth.username, auth.password)
        print(user)
        if user:
            userid = await get_userid(auth.username, auth.password)
            print("user id type", type(userid))
            db = await _get_db()
            secret_word = await db.fetch_all("SELECT correctword FROM Correct_Words")
            secret_word = random.choice(secret_word)
            print("secret word type",type(secret_word))
            query1 = "INSERT INTO Games(userid, secretword) VALUES (:userid, :secretword)"
            values1 = {"userid": userid[0] , "secretword": secret_word[0]}

            print("print values***************",values1)
        
            gameid = await db.execute("INSERT INTO Games(userid, secretword) VALUES (:userid, :secretword)", values={"userid": userid[0] , "secretword": secret_word[0]})
            print(gameid)
            if gameid:
                return {"Location": f"/newgame/{gameid}"},201
            else:
                abort(417)

        else:
            # return "could not verify user",401,{'WWW-Authenticate':'Basic realm="MyApp"'}
            abort(401)
    else:
        return "could not verify user",401,{'WWW-Authenticate':'Basic realm="MyApp"'}


@app.errorhandler(417)
def not_found(e):
    return {"error":"New game creation failed"}, 417



@app.route("/guess/<string:word>", methods=["POST"])
async def guess(word):
    auth = request.authorization
    
    if auth:
        user= await authenticate_user(auth.username, auth.password)
        
        if user:
            userid = await get_userid(auth.username, auth.password)
            print("user id type", type(userid))
            db = await _get_db()
            

        else: 
            # return "could not verify user",401,{'WWW-Authenticate':'Basic realm="MyApp"'}
            abort(401)
    else:
        return "could not verify user",401,{'WWW-Authenticate':'Basic realm="MyApp"'}

    
    
    



@app.route("/inprogressgame", methods=["GET"])
async def get_inprogressgame():
    return textwrap.dedent(
        """
        <h1>At List of inprogress games API</h1>

        """
    )

@app.route("/gamestaus/<int:gameid>", methods=["GET"])
async def game_status(gameid):
    return textwrap.dedent(
        """
        <h1>At game status API</h1>

        """
    )









