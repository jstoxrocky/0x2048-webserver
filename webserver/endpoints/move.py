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
    PaymentRequired,
)
from webserver import (
    state_channel,
)
from webserver.gameplay import (
    load,
    new,
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
    ARCADE_ADDR,
)
from webserver.schemas import (
    MoveSchema,
)


blueprint = Blueprint('move', __name__)


@blueprint.route('/move', methods=['POST'])
@cross_origin(origins=ORIGINS, methods=['POST'], supports_credentials=True)
def move():
    # Validate payload
    payload = request.get_json()
    if MoveSchema().validate(payload):
        raise ValidationError
    if not session.get('has_paid', False):
        raise PaymentRequired
    # Load game
    state = session.get('state', INITIAL_STATE)
    state = new() if state['gameover'] else load(state, payload['direction'])
    # Create state-channel signature
    msg = state_channel.solidity_keccak(
        ARCADE_ADDR,
        payload['user'],
        state['score'],
    )
    signature = state_channel.sign(msg, PRIV)
    session['state'] = merge(state, {'signature': signature})
    return jsonify(session['state'])
