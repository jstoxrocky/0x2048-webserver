import json
import redis
from webserver.arcade import (
    Arcade,
)
from webserver.exceptions import (
    AddressPayloadValidationError,
    UnpaidSessionValidationError,
)
from webserver.schemas import (
    UnpaidSession,
    AddressPayload,
)
from webserver.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)


def game(payload):
    errors = AddressPayload().validate(payload)
    if errors:
        raise AddressPayloadValidationError

    # Validate session
    session_id = payload['session_id']
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    serialized_session = sessions.get(session_id) or '{}'
    session = json.loads(serialized_session)
    errors = UnpaidSession().validate(session)
    if errors:
        raise UnpaidSessionValidationError

    # Confirm payment
    gamecode = session['gamecode']
    address = payload['address']
    error = Arcade.confirm_payment(address, gamecode)
    if error:
        raise error

    # Start new game
    arcade = Arcade(player=address)
    next_state, signature = arcade.new_game()

    # Set session
    session_data = {
        'paid': True,
        'gamestate': next_state,
        'address': address,
    }
    sessions.set(session_id, json.dumps(session_data))

    # Set payload
    payload = {
        'session_id': session_id,
        'gamestate': next_state,
        'signature': signature,
    }
    return json.dumps(payload)
