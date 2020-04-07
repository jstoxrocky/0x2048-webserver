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

# we cant allow users to tell us what the session is here
# they can overwrite someone elses that way.

def move(move_payload):
    errors = Move().validate(move_payload)
    if errors:
        raise MoveValidationError

    # Validate session
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    gamecode = move_payload['gamecode']
    serialized_session = sessions.get(gamecode) or '{}'
    session = json.loads(serialized_session)
    errors = PaidSession().validate(session)
    if errors:
        raise PaidSessionValidationError

    # Move
    address = session['address']
    updated_game = Arcade.update_game(
        address,
        current_state=session['gamestate'],
        update=move_payload['direction'],
    )

    session_data = {
        'paid': True,
        'gamestate': updated_game['state'],
        'address': address,
    }
    sessions.set(gamecode, json.dumps(session_data))
    payload = {
        'gamecode': gamecode,
        'gamestate': updated_game['state'],
        'signature': updated_game['signed_score'],
    }
    return json.dumps(payload)
