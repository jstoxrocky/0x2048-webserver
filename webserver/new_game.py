import json
import redis
from webserver.arcade import (
    Arcade,
)
from webserver.exceptions import (
    ChallengeResponseValidationError,
    UnpaidSessionValidationError,
    PaymentError,
)
from webserver.schemas import (
    UnpaidSession,
    ChallengeResponse,
)
from webserver.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)


def new_game(event, context):
    # Validate challenge response
    challenge_response = event
    errors = ChallengeResponse().validate(challenge_response)
    if errors:
        raise ChallengeResponseValidationError

    # Validate session
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    session_id = challenge_response['session_id']
    serialized_session = sessions.get(session_id) or '{}'
    session = json.loads(serialized_session)
    errors = UnpaidSession().validate(session)
    if errors:
        raise UnpaidSessionValidationError

    # Confirm payment
    # should this change to Arcade.confirm_payment(address, challenge)...?
    payment_confirmation = Arcade.confirm_payment(
        session['challenge'],
        challenge_response['signature']['v'],
        challenge_response['signature']['r'],
        challenge_response['signature']['s'],
    )
    if not payment_confirmation['success']:
        raise PaymentError

    # Start new game
    arcade = Arcade(player_address=payment_confirmation['recovered_address'])
    signed_gamestate = arcade.new_game()

    session_data = {
        'paid': True,
        'gamestate': signed_gamestate['state'],
        'recovered_address': payment_confirmation['recovered_address'],
    }
    sessions.set(session_id, json.dumps(session_data))
    payload = {
        'session_id': session_id,
        'gamestate': signed_gamestate['state'],
        'signature': signed_gamestate['signed_score'],
    }
    return json.dumps(payload)
