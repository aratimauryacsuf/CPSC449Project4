
import collections
import dataclasses
import textwrap
import sqlite3
import databases
import toml

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
    user = dataclasses.asdict(data)
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

@app.route("/user/login/<string:username>/<string:password>")
async def login(username, password):
    # db = await _get_db()
    user = await authenticate_user(username,password)
    if user:
        return textwrap.dedent(
        """
        <h1>Welcome to the Wordle</h1>

        """
    )
    else:
        abort(401)
    

@app.errorhandler(401)
def not_found(e):
    return {"error": "Unauthorized"}, 401


async def authenticate_user(username,password):
    db = await _get_db()
    user = await db.fetch_one("select * from user")
    # user = db.fetch_one(f"SELECT * FROM user WHERE username = :{username} AND userpassword = :{password}", values={"{username}": {username}, "{password}":{password}})
    return user

@app.route("/login")
async def authLogin():
    print("Request auth value" + str(request.authorization))
    if not request.authorization:
        return "could not verify user",401,{'WWW-Authenticate':'Basic relam="Need username and password"'}
    else:
        auth = request.authorization
        user= await authenticate_user(auth.username, auth.password)
    return "Login successful"

# End of User API
    
# Start of Game API
    
@app.route("/newgame")
async def creat_newgame():
    return textwrap.dedent(
        """
        <h1>At new game API</h1>

        """
    )


@app.route("/guess")
async def guess():
    return textwrap.dedent(
        """
        <h1>At Guess Word  API</h1>

        """
    )

@app.route("/inprogressgame")
async def get_inprogressgame():
    return textwrap.dedent(
        """
        <h1>At List of inprogress games API</h1>

        """
    )

@app.route("/gamestaus")
async def game_status():
    return textwrap.dedent(
        """
        <h1>At game status API</h1>

        """
    )









