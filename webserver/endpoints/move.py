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
    ARCADE_ADDR,
)
from webserver.schemas import (
    MoveSchema,
)


blueprint = Blueprint('move', __name__)


@blueprint.route('/move', methods=['POST'])
@cross_origin(origins=ORIGINS, methods=['POST'], supports_credentials=True)
def move():
    # Ensure user has already paid
    if not session.get('has_paid', False):
        raise PaymentRequired
    # Validate payload
    payload = request.get_json()
    if MoveSchema().validate(payload):
        raise ValidationError
    # Load game
    state = session.get('state', INITIAL_STATE)
    state = next_state(state, payload['direction'], state['gameover'])
    # Reset payment to False on gameover
    if state['gameover']:
        session['has_paid'] = False
    # Create state-channel signature
    msg = state_channel.solidity_keccak(
        ARCADE_ADDR,
        payload['user'],
        state['score'],
    )
    signature = state_channel.sign(msg, PRIV)
    session['state'] = merge(state, {'signature': signature})
    return jsonify(session['state'])
