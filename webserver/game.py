import json
import redis
from webserver.arcade import (
    Arcade,
)
from webserver.exceptions import (
    PaymentLocatorPayloadValidationError,
    UnpaidSessionValidationError,
    PaymentError,
)
from webserver.schemas import (
    UnpaidSession,
    PaymentLocatorPayload,
)
from webserver.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)
from game.game import (
    TwentyFortyEight,
)


def game(payload):
    errors = PaymentLocatorPayload().validate(payload)
    if errors:
        raise PaymentLocatorPayloadValidationError

    # Validate session
    session_id = payload['session_id']
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    serialized_session = sessions.get(session_id) or '{}'
    session = json.loads(serialized_session)
    error = UnpaidSession().validate(session)
    if error:
        raise UnpaidSessionValidationError

    # Confirm payment
    payment_code = session['payment_code']
    address = payload['address']
    arcade = Arcade(player=address, game=TwentyFortyEight)
    error = arcade.confirm_payment(payment_code)
    if error:
        raise PaymentError

    # Start new game
    next_state, signed_score = arcade.new_game()

    # Set session
    session_data = {
        'paid': True,
        'gamestate': next_state,
        'address': address,
    }
    sessions.set(session_id, json.dumps(session_data))

    # Set payload
    payload = {
        'gamestate': next_state,
        'signed_score': signed_score,
    }
    return json.dumps(payload)
