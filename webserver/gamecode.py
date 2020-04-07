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


def gamecode():
    '''
    Reset session data with new session ID and gamecode
    Send gamecode and session_id "cookie" back to client
    '''
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    gamecode = Arcade.new_gamecode()
    session_id = Arcade.new_session_id()
    session_data = {
        'paid': False,
        'gamecode': gamecode,
    }
    sessions.set(session_id, json.dumps(session_data))
    payload = {
        'session_id': session_id,
        'gamecode': gamecode,
    }
    return json.dumps(payload)
