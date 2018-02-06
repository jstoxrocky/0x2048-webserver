from flask import (
    jsonify,
    session,
    Blueprint,
)
from flask_cors import (
    cross_origin,
)
from webserver.config import (
    ORIGINS,
    INITIAL_STATE,
)


blueprint = Blueprint('gamestate', __name__)


@blueprint.route('/gamestate', methods=['GET'])
@cross_origin(origins=ORIGINS, methods=['GET'], supports_credentials=True)
def gamestate():
    state = session.get('state', INITIAL_STATE)
    return jsonify(state)
