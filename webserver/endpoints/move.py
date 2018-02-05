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
    MissingUser,
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
)
from eth_utils import (
    is_checksum_address,
)
from toolz.dicttoolz import (
    merge,
)
from webserver.config import (
    PRIV,
    ADDR,
)


INITIAL_STATE = {'board': [], 'score': 0, 'gameover': True}
blueprint = Blueprint('move', __name__)


@blueprint.route('/move', methods=['POST'])
@cross_origin(origins=ORIGINS, methods=['POST'], supports_credentials=True)
def move():
    # Get payload from user
    payload = request.get_json()
    user = payload.get('user')
    direction = payload.get('direction')
    # State-channel signature requires a user's address
    if not is_checksum_address(user):
        raise MissingUser
    # Load game
    state = session.get('state', INITIAL_STATE)
    state = new() if state['gameover'] else load(state, direction)
    session['state'] = state
    # Create state-channel signature
    signature = state_channel.sign(PRIV, ADDR, user, session['state']['score'])
    return jsonify(merge(state, {'signature': signature}))
