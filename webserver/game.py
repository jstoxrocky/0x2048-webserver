import json
import redis
from webserver.arcade import (
    Arcade,
)
from webserver.exceptions import (
    SignaturePayloadValidationError,
    UnpaidSessionValidationError,
    PaymentError,
)
from webserver.schemas import (
    UnpaidSession,
    SignaturePayload,
)
from webserver.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)


def game(signature_payload):
    # Validate gamecode response
    errors = SignaturePayload().validate(signature_payload)
    if errors:
        raise SignaturePayloadValidationError

    # Validate session
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    session_id = signature_payload['session_id']
    serialized_session = sessions.get(session_id) or '{}'
    session = json.loads(serialized_session)
    errors = UnpaidSession().validate(session)
    if errors:
        raise UnpaidSessionValidationError

    # Confirm payment
    gamecode = session['gamecode']
    address = Arcade.recover_signer(gamecode, **signature_payload['signature'])
    success = Arcade.confirm_payment(
        address,
        gamecode,
    )
    if not success:
        raise PaymentError

    # Start new game
    signed_gamestate = Arcade.new_game(address)

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
