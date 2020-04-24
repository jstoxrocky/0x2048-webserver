import os
import json
import redis
import arcade_protocol
from web3.providers import (
    HTTPProvider,
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
    ADDRESS,
    ABI,
    KEY,
)
from game.game import (
    TwentyFortyEight,
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

    # Arcade protocol
    user = session['user']
    INFURA_PROJECT_ID = os.environ['INFURA_PROJECT_ID']
    INFURA_PROJECT_SECRET = os.environ['INFURA_PROJECT_SECRET']
    headers = {"auth": ("", INFURA_PROJECT_SECRET)}
    uri = 'https://ropsten.infura.io/v3/%s' % (INFURA_PROJECT_ID)
    provider = HTTPProvider(uri, headers)
    contract = arcade_protocol.Contract(provider, ADDRESS, ABI)
    game_interface = arcade_protocol.GameInterface(
        contract,
        game_id=TwentyFortyEight.id,
        player=user,
    )

    # Move
    state = session['gamestate']
    direction = payload['direction']
    next_state = TwentyFortyEight.update(state, direction)
    signed_score = game_interface.sign(KEY, next_state['score'])

    # Set session
    session_data = {
        'paid': True,
        'gamestate': next_state,
        'user': user,
    }
    sessions.set(session_id, json.dumps(session_data))

    # Set payload
    payload = {
        'gamestate': next_state,
        'signed_score': signed_score,
    }
    return json.dumps(payload)
