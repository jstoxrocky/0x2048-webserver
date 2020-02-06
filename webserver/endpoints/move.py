from flask import (
    jsonify,
    request,
    session,
    Blueprint,
)
from flask_cors import (
    cross_origin,
)
from webserver import exceptions
from webserver import (
    signing,
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
    # Ensure user has already paid
    if not session.get('paid', False):
        raise exceptions.UnexpectedMoveAttemptWithoutPaying
    # Validate payload
    payload = request.get_json()
    if schemas.Move().validate(payload):
        raise exceptions.ValidationError
    # Load game
    state = session.get('state', INITIAL_STATE)
    new_state = next_state(state, payload['direction'])
    # Create state-channel signature
    signed_score = signing.sign_score(
        PRIV,
        ARCADE_ADDRESS,
        session['recoveredAddress'],
        new_state['score'],
    )
    session['state'] = merge(
        new_state, {
            'signature': signed_score,
            'recoveredAddress': session['recoveredAddress'],
        }
    )
    return jsonify(session['state'])
