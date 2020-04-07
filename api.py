from flask import (
    request,
    Blueprint,
)
from webserver.new_gamecode import (
    new_gamecode as endpoints_new_gamecode,
)
from webserver.new_game import (
    new_game as endpoints_new_game,
)
from webserver.move import (
    move as endpoints_move,
)


api = Blueprint('api', __name__)


@api.route('/gamecode', methods=['GET'])
def gamecode():
    payload = endpoints_new_gamecode()
    return payload


@api.route('/new_game', methods=['POST'])
def new_game():
    event = request.get_json()
    payload = endpoints_new_game(event)
    return payload


@api.route('/move', methods=['POST'])
def move():
    event = request.get_json()
    payload = endpoints_move(event)
    return payload
