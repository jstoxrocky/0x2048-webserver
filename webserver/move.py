import json
import redis
from webserver.arcade import (
    Arcade,
)
from webserver.exceptions import (
    MovePayloadValidationError,
    PaidSessionValidationError,
)
from webserver.schemas import (
    MovePayload,
    PaidSession,
)
from webserver.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)


def move(payload):
    errors = MovePayload().validate(payload)
    if errors:
        raise MovePayloadValidationError

    # Validate session
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    session_id = payload['session_id']
    serialized_session = sessions.get(session_id) or '{}'
    session = json.loads(serialized_session)
    errors = PaidSession().validate(session)
    if errors:
        raise PaidSessionValidationError

    # Move
    address = session['address']
    game_id = session['game_id']
    current_state = session['gamestate']
    update = payload['direction']
    arcade = Arcade(player=address)
    next_state, signed_score = arcade.update_game(
        game_id,
        current_state,
        update,
    )

    # Set session
    session_data = {
        'paid': True,
        'gamestate': next_state,
        'address': address,
        'game_id': game_id,
    }
    sessions.set(session_id, json.dumps(session_data))

    # Set payload
    payload = {
        'gamestate': next_state,
        'signed_score': signed_score,
    }
    return json.dumps(payload)
