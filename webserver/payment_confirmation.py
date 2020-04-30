import os
import json
import redis
import arcade_protocol
from web3.providers import (
    HTTPProvider,
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
    ADDRESS,
    ABI,
    KEY,
)
from game.game import (
    TwentyFortyEight,
)


def payment_confirmation(payload):
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

    # Arcade protocol
    user = payload['user']
    INFURA_PROJECT_ID = os.environ['INFURA_PROJECT_ID']
    INFURA_PROJECT_SECRET = os.environ['INFURA_PROJECT_SECRET']
    headers = {"auth": ("", INFURA_PROJECT_SECRET)}
    uri = 'https://ropsten.infura.io/v3/%s' % (INFURA_PROJECT_ID)
    provider = HTTPProvider(uri, headers)
    contract = arcade_protocol.Contract(
        provider,
        ADDRESS,
        ABI,
        TwentyFortyEight.id,
    )
    game_interface = arcade_protocol.GameInterface(
        contract,
        player=user,
    )

    # Confirm payment
    payment_code = session['payment_code']
    error = game_interface.confirm_payment(payment_code)
    if error:
        raise PaymentError

    # Start new game
    state = TwentyFortyEight.new()
    signed_score = game_interface.sign(KEY, state['score'])

    # Set session
    session_data = {
        'paid': True,
        'gamestate': state,
        'user': user,
    }
    sessions.set(session_id, json.dumps(session_data))

    # Set payload
    payload = {
        'gamestate': state,
        'signed_score': signed_score,
    }
    return json.dumps(payload)
