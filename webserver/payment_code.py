import json
import redis
from arcade_protocol import (
    GameInterface,
)
from webserver.config import (
    REDIS_URL
)
from webserver.session import (
    new_session,
)


def payment_code():
    '''
    Reset session data with new session ID and payment_code
    Send payment_code and session_id "cookie" back to client
    '''
    sessions = redis.Redis.from_url(REDIS_URL)

    payment_code = GameInterface.new_payment_code()
    session_id = new_session()

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
