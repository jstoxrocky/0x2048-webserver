from flask import (
    request,
    Blueprint,
)
from webserver.payment_code import (
    payment_code as endpoints_payment_code,
)
from webserver.payment_confirmation import (
    payment_confirmation as endpoints_payment_confirmation,
)
from webserver.move import (
    move as endpoints_move,
)


api = Blueprint('api', __name__)


@api.route('/payment_code', methods=['GET'])
def payment_code():
    payload = endpoints_payment_code()
    return payload


@api.route('/payment_confirmation', methods=['GET'])
def payment_confirmation():
    session_id = request.args.get('session_id')
    user = request.args.get('user')
    args = {
        'user': user,
        'session_id': session_id,
    }
    payload = endpoints_payment_confirmation(args)
    return payload


@api.route('/move', methods=['POST'])
def move():
    move_payload = request.get_json()
    payload = endpoints_move(move_payload)
    return payload
