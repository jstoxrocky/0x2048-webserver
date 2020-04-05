from flask import (
    request,
    Blueprint,
)
from webserver.new_session import (
    new_session as endpoints_new_session,
)
from webserver.new_game import (
    new_game as endpoints_new_game,
)
from webserver.move import (
    move as endpoints_move,
)


api = Blueprint('api', __name__)


@api.route('/new_session', methods=['GET'])
def new_session():
    payload = endpoints_new_session(None, None)
    return payload


@api.route('/new_game', methods=['POST'])
def new_game():
    event = request.get_json()
    payload = endpoints_new_game(event, None)
    return payload


@api.route('/move', methods=['POST'])
def move():
    event = request.get_json()
    payload = endpoints_move(event, None)
    return payload
