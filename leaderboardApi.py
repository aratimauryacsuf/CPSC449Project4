import textwrap
import dataclasses
from quart import Quart, abort, g, request
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

import redis

app = Quart(__name__)
QuartSchema(app)

# app.config.from_file(f"./etc/{__name__}.toml", toml.load)

# game_result=redis.Redis(host="http://127.0.0.1", port=5200,db=0)
redis_db=redis.Redis(host="localhost", port=6379, db=0)

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
@validate_request(result)
def report_result(data):
    result =dataclasses.asdict(data)
    # # result ={"username":"PQR", "game_status":"WIN", "guess_count":4}
    # print(result)
    print(redis_db.hexists(result["username"]),"score")
    score =0
    
    if(result["game_status"].lower()== 'win') and (result["guess_count"]== 6):
        score +=1
    elif (result["game_status"].lower()== 'win') and (result["guess_count"]== 5):
        score += 2
    elif (result["game_status"].lower()== 'win') and (result["guess_count"]== 4):
        score+=3
    elif (result["game_status"].lower()== 'win') and (result["guess_count"]== 3):
        score += 4
    elif (result["game_status"].lower()== 'win') and (result["guess_count"]== 2):
        score+= 5
    elif (result["game_status"].lower()== 'win') and (result["guess_count"]== 1):
        score += 6
    else:
        score += 0
    redis_db.hset(result["username"], "game_status", result["game_status"])
    redis_db.hset(result["username"], "guess_count", result["guess_count"])
    print(redis_db.hget(result["username"],"game_status"))
    # redis_db.hset(result["username"], "score", 100)

    # redis_db.hset("user2", "game_status", "loss")
    # redis_db.hset("user2", "guess_count", 6)
    # redis_db.hset("user2", "score", 200)
    
    # outcome=game_result.mset({"username":result["username"], "game_status":result["game_status"],"guess_count":result["guess_count"] })
    keys = redis_db.keys()
    print(keys)

    for key in keys:
        print(redis_db.hgetall(key))
    
    
    # testresult=game_result.GETSET("username")
    # print(testresult)
    return "result added"


