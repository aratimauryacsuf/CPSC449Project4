import textwrap
import dataclasses
from quart import Quart, abort, g, request
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

import redis

app = Quart(__name__)
QuartSchema(app)

# app.config.from_file(f"./etc/{__name__}.toml", toml.load)

# game_result=redis.Redis(host="http://127.0.0.1", port=5200,db=0)
game_result=redis.Redis(host="localhost", port=6379)

@dataclasses.dataclass
class result:
    username: str
    game_status: str
    guess_count: int


@app.route("/")
def index():
    return textwrap.dedent(
        """
        <h1>Welcome to the Leaderboard API</h1>

        """
    )

@app.route("/report_result", methods=["POST"])
# @validate_request(result)
def report_result():
    # # result ={"username":"PQR", "game_status":"WIN", "guess_count":4}
    # print(result)
   
    # outcome=game_result.mset({"username":result["username"], "game_status":result["game_status"],"guess_count":result["guess_count"] })
    keys = game_result.keys()
    print(keys)
    # testresult=game_result.GETSET("username")
    # print(testresult)



