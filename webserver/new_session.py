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


def new_session(event, context):
    '''
    Reset session data with new session ID and challenge
    Send challenge and session_id "cookie" back to client
    '''
    print(1)
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    print(2)
    arcade_response = Arcade.new_session()
    print(3)
    session_data = {
        'paid': False,
        'challenge': arcade_response['challenge']
    }
    print(4)
    sessions.set(arcade_response['session_id'], json.dumps(session_data))
    print(5)
    payload = {
        'session_id': arcade_response['session_id'],
        'challenge': arcade_response['challenge'],
    }
    print(6)
    return json.dumps(payload)
