user: hypercorn UsersApi --reload --debug --bind UsersApi.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
game_primary: ./bin/litefs --config ./etc/game_primary.yml
# game1: hypercorn WordleGameApi --reload --debug --bind WordleGameApi.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
game_secondary_1: ./bin/litefs --config ./etc/game_secondary_1.yml
# game2: hypercorn WordleGameApi --reload --debug --bind WordleGameApi.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
game_secondary_2: ./bin/litefs --config ./etc/game_secondary_2.yml
# game3: hypercorn WordleGameApi --reload --debug --bind WordleGameApi.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
# leaderboard: hypercorn leaderboardApi --reload --debug --bind leaderboardApi.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
