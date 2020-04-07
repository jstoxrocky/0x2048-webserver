import json
import redis
from webserver.arcade import (
    Arcade,
)
from webserver.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)

# Accepts: nothing
# Must have: nothing
# Sets:
# - session
# -- paid: false
# - payload
# -- gamecode
def new_gamecode():
    '''
    Reset session data with new gamecode
    Send gamecode back to client
    '''
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    gamecode = Arcade.new_gamecode()
    session = {
        'paid': False,
    }
    sessions.set(gamecode, json.dumps(session))
    payload = {
        'gamecode': gamecode,
    }
    return json.dumps(payload)
