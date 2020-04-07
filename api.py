from flask import (
    request,
    Blueprint,
)
from webserver.gamecode import (
    gamecode as endpoints_gamecode,
)
from webserver.game import (
    game as endpoints_game,
)
from webserver.move import (
    move as endpoints_move,
)


api = Blueprint('api', __name__)


@api.route('/gamecode', methods=['GET'])
def gamecode():
    payload = endpoints_gamecode()
    return payload


@api.route('/game', methods=['GET'])
def game():
    signature_payload = request.get_json()
    payload = endpoints_game(signature_payload)
    return payload


@api.route('/move', methods=['POST'])
def move():
    move_payload = request.get_json()
    payload = endpoints_move(move_payload)
    return payload
