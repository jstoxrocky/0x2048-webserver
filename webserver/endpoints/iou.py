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


blueprint = Blueprint('iou', __name__)


class mock_db_connection:
    value = 7

    @classmethod
    def execute(cls, query):
        return cls.value


@blueprint.route('/nonce', methods=['GET'])
@cross_origin(origins=ORIGINS, methods=['GET'],
              supports_credentials=True)
def nonce():
    # Validate payload
    payload = request.args
    if UserSchema().validate(payload):
        raise ValidationError
    # Get most recent value
    db_value = mock_db_connection.execute("""SELECT * FROM tbl;""")
    return jsonify({'value': db_value})


@blueprint.route('/iou', methods=['POST'])
@cross_origin(origins=ORIGINS, methods=['POST'],
              supports_credentials=True)
def iou():
    # Ensure user has not already paid
    if session.get('has_paid', False):
        raise UnexpectedPayment
    # Validate payload
    payload = request.get_json()
    if IOUSchema().validate(payload):
        raise ValidationError
    # Validate IOU
    success = state_channel.validate_iou(payload)
    if not success:
        raise UnexpectedSignature
    # Ensure the preimage value is strictly greater than the db value
    db_value = mock_db_connection.execute("""SELECT * FROM tbl;""")
    if payload['value'] <= db_value:
        raise IOUPaymentTooLow
    # TODO:
    # Store IOU in db
    # Start a new game
    session['has_paid'] = True
    new_state = new()
    msg = state_channel.solidity_keccak(
        ARCADE_ADDR,
        payload['user'],
        new_state['score'],
    )
    signature = state_channel.sign(msg, PRIV)
    session['state'] = merge(new_state, {'signature': signature})
    return jsonify(session['state'])
