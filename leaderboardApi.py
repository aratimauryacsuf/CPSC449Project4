import textwrap
import dataclasses
from quart import Quart, abort, g, request
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

import redis

app = Quart(__name__)
QuartSchema(app)


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
    
    if(result["game_status"].lower()== 'win') and (result["guess_count"]== 6):
        score =1
    elif (result["game_status"].lower()== 'win') and (result["guess_count"]== 5):
        score = 2
    elif (result["game_status"].lower()== 'win') and (result["guess_count"]== 4):
        score=3
    elif (result["game_status"].lower()== 'win') and (result["guess_count"]== 3):
        score = 4
    elif (result["game_status"].lower()== 'win') and (result["guess_count"]== 2):
        score= 5
    elif (result["game_status"].lower()== 'win') and (result["guess_count"]== 1):
        score = 6
    elif (result["game_status"].lower()== 'loss') and (result["guess_count"]== 6):
        score = 0
    else:
        return "Please enter game status win or loss and guess count between 1 and 6"
        
 
    redis_db.lpush(result["username"],score)

    list_elements=redis_db.lrange(result["username"],0,-1)
  
    print("list element"+ str(list_elements))
    total_score= 0
    for element in list_elements:
        print(element)
        total_score+=int(element)
    
    print("total score"+ str(total_score))

    avg_score= total_score / len(list_elements)
    print(avg_score)

    redis_db.zadd("Users", {result["username"]: avg_score})
    users = redis_db.zrevrange("Users", 0, -1, withscores=True)
    print(users)

    
    return "Game result added"


