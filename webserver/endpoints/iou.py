from flask import (
    jsonify,
    Blueprint,
    session,
    request,
)
from flask_cors import (
    cross_origin,
)
from webserver.config import (
    ORIGINS,
    PRIV,
    ARCADE_ADDR,
)
from webserver.exceptions import (
    ValidationError,
    IOUPaymentTooLow,
    UnexpectedPayment,
    UnexpectedSignature,
    NoTimeLeft,
    NoValueLeft,
)
from webserver import (
    state_channel,
)
from webserver.schemas import (
    IOUSchema,
    UserSchema,
)
from webserver.gameplay import (
    new,
)
from toolz.dicttoolz import (
    merge,
)
from webserver.db import (
    get_latest_nonce,
    insert_iou,
)
from webserver.chain import (
    calc_net_time_left,
    calc_net_balance,
)


blueprint = Blueprint('iou', __name__)


@blueprint.route('/nonce', methods=['GET'])
@cross_origin(origins=ORIGINS, methods=['GET'],
              supports_credentials=True)
def nonce():
    # Validate payload
    payload = request.args
    if UserSchema().validate(payload):
        raise ValidationError
    # Get most recent value
    nonce = get_latest_nonce(payload['user'])
    return jsonify({'nonce': nonce})


@blueprint.route('/iou', methods=['POST'])
@cross_origin(origins=ORIGINS, methods=['POST'],
              supports_credentials=True)
def iou():
    # Ensure user has not already paid
    if session.get('has_paid', False):
        raise UnexpectedPayment
    # Validate that request data is an iou
    iou = request.get_json()
    if IOUSchema().validate(iou):
        raise ValidationError
    # Verfiy signature
    success = state_channel.validate_iou(iou)
    if not success:
        raise UnexpectedSignature
    # Ensure the nonce is strictly greater than the db nonce
    nonce = get_latest_nonce(iou['user'])
    if iou['nonce'] <= nonce:
        raise IOUPaymentTooLow
    # Ensure the user has time left on their onchain account
    net_time_left = calc_net_time_left()
    if net_time_left <= 0:
        raise NoTimeLeft
    # Endsure the user has value left in their onchain account
    net_balance = calc_net_balance()
    if net_balance <= 0:
        raise NoValueLeft
    # Store IOU in db
    insert_iou(**iou)
    # Start a new game
    session['has_paid'] = True
    new_state = new()
    msg = state_channel.solidity_keccak(
        ARCADE_ADDR,
        iou['user'],
        new_state['score'],
    )
    signature = state_channel.sign(msg, PRIV)
    session['state'] = merge(new_state, {'signature': signature})
    return jsonify(session['state'])
