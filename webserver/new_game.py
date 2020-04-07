import json
import redis
from webserver.arcade import (
    Arcade,
)
from webserver.exceptions import (
    AuthenticationResponseValidationError,
    UnpaidSessionValidationError,
    PaymentError,
)
from webserver.schemas import (
    UnpaidSession,
    AuthenticationResponse,
)
from webserver.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)


# we have in Flaks session
# should not send back gamecode here

# Accepts: sign(gamecode)
# Must have:
# - sign(gamecode)
# - session paid: false
# Sets:
# - session
# -- paid: true
# -- gamestate
# -- user
# - payload
# -- gamestate
# -- signature
def new_game(auth):
    # Validate identity_authentication
    errors = AuthenticationResponse().validate(auth)
    if errors:
        raise AuthenticationResponseValidationError

    # Validate session
    sessions = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    gamecode = auth['gamecode']
    serialized_session = sessions.get(gamecode) or '{}'
    session = json.loads(serialized_session)
    errors = UnpaidSession().validate(session)
    if errors:
        raise UnpaidSessionValidationError

    # Confirm payment
    address = Arcade.recover_signer(gamecode, **auth['signature'])
    success = Arcade.confirm_payment(
        address,
        gamecode,
    )
    if not success:
        raise PaymentError

    # Start new game
    new_game = Arcade.new_game(address)
    session_data = {
        'paid': True,
        'gamestate': new_game['state'],
        'address': address,
    }
    sessions.set(gamecode, json.dumps(session_data))
    payload = {
        'gamecode': gamecode,
        'gamestate': new_game['state'],
        'signature': new_game['signed_score'],
    }
    return json.dumps(payload)
