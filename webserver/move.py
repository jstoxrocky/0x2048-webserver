import json
import redis
from webserver.arcade import (
    Arcade,
)
from webserver.exceptions import (
    MoveValidationError,
    PaidSessionValidationError,
)
from webserver.schemas import (
    Move,
    PaidSession,
)
from webserver.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)


def move(move_payload):
    # Validate gamecode response
    errors = Move().validate(move_payload)
    if errors:
        raise MoveValidationError

    # Validate session
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    session_id = move_payload['session_id']
    serialized_session = sessions.get(session_id) or '{}'
    session = json.loads(serialized_session)
    errors = PaidSession().validate(session)
    if errors:
        raise PaidSessionValidationError

    # Move
    address = session['address']
    signed_gamestate = Arcade.update_game(
        current_state=session['gamestate'],
        update=move_payload['direction'],
        address=address,
    )

    session_data = {
        'paid': True,
        'gamestate': signed_gamestate['state'],
        'address': address,
    }
    sessions.set(session_id, json.dumps(session_data))
    payload = {
        'session_id': session_id,
        'gamestate': signed_gamestate['state'],
        'signature': signed_gamestate['signed_score'],
    }
    return json.dumps(payload)
