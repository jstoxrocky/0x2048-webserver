from flask import (
    request,
    Blueprint,
)
from webserver.payment_code import (
    payment_code as endpoints_payment_code,
)
from webserver.game import (
    game as endpoints_game,
)
from webserver.move import (
    move as endpoints_move,
)


api = Blueprint('api', __name__)


@api.route('/payment_code', methods=['GET'])
def payment_code():
    payload = endpoints_payment_code()
    return payload


@api.route('/game', methods=['GET'])
def game():
    session_id = request.args.get('session_id')
    address = request.args.get('address')
    args = {
        'address': address,
        'session_id': session_id,
    }
    payload = endpoints_game(args)
    return payload


@api.route('/move', methods=['POST'])
def move():
    move_payload = request.get_json()
    payload = endpoints_move(move_payload)
    return payload
