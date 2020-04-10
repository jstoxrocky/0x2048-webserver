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


def payment_code():
    '''
    Reset session data with new session ID and payment_code
    Send payment_code and session_id "cookie" back to client
    '''
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    payment_code = Arcade.new_payment_code()
    session_id = Arcade.new_session_id()

    # This is the only place that payment_code gets
    # set in the session. For this reason, we can
    # skip the user signing and sending us their signature since
    # we need whatever address they send us (could be a lie) to match
    # with the session payment_code.
    session_data = {
        'paid': False,
        'payment_code': payment_code,
    }
    sessions.set(session_id, json.dumps(session_data))
    payload = {
        'session_id': session_id,
        'payment_code': payment_code,
    }
    return json.dumps(payload)
