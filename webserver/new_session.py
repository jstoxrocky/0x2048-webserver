import json
import redis
from webserver.arcade import (
    Arcade,
)
from webserver.config import (
    REDIS_HOST,
    REDIS_PORT,
)


def new_session(event, context):
    '''
    Reset session data with new session ID and challenge
    Send challenge and session_id "cookie" back to client
    '''
    sessions = redis.Redis(REDIS_HOST, REDIS_PORT)
    arcade_response = Arcade.new_session()
    session_data = {
        'paid': False,
        'challenge': arcade_response['challenge']
    }
    sessions.set(arcade_response['session_id'], json.dumps(session_data))
    payload = {
        'session_id': arcade_response['session_id'],
        'challenge': arcade_response['challenge'],
    }
    return json.dumps(payload)
