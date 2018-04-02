from flask import (
    jsonify,
    request,
    session,
    Blueprint,
)
from flask_cors import (
    cross_origin,
)
from webserver.exceptions import (
    ValidationError,
)
from webserver import (
    state_channel,
)
from webserver.gameplay import (
    next_state,
)
from webserver.config import (
    ORIGINS,
    INITIAL_STATE,
)
from toolz.dicttoolz import (
    merge,
)
from webserver.config import (
    PRIV,
    ARCADE_ADDRESS,
)
from webserver import schemas


blueprint = Blueprint('move', __name__)


@blueprint.route('/move', methods=['POST'])
@cross_origin(origins=ORIGINS, methods=['POST'], supports_credentials=True)
def move():
    # Validate payload
    payload = request.get_json()
    if schemas.Move().validate(payload):
        raise ValidationError
    # Load game
    state = session.get('state', INITIAL_STATE)
    new_state = next_state(state, payload['direction'])
    # Create state-channel signature
    msg = state_channel.solidity_keccak(
        ARCADE_ADDRESS,
        payload['user'],
        new_state['score'],
    )
    signature = state_channel.sign(msg, PRIV)
    session['state'] = merge(new_state, {'signature': signature})
    return jsonify(session['state'])
