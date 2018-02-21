from flask import (
    jsonify,
    Blueprint,
    request,
)
from flask_cors import (
    cross_origin,
)
from webserver.config import (
    ORIGINS,
)
from webserver.exceptions import (
    ValidationError,
    UnexpectedPreimage,
    UnexpectedSigner,
    IOUPaymentTooLow,
)
from webserver.config import (
    ACCOUNT_ADDR,
)
from webserver import (
    state_channel,
)
from webserver.schemas import (
    SignatureSchema,
)


blueprint = Blueprint('iou', __name__)


class mock_db_connection:
    value = 7

    @classmethod
    def execute(cls, query):
        return cls.value


@blueprint.route('/iou', methods=['POST'])
@cross_origin(origins=ORIGINS, methods=['POST'], supports_credentials=True)
def iou():
    # Validate payload
    payload = request.get_json()
    if SignatureSchema().validate(payload):
        raise ValidationError
    # Do the preimages hash together to form the signed message
    expected_msg = state_channel.solidityKeccak(
        ACCOUNT_ADDR,
        payload['user'],
        payload['value'],
    )
    if expected_msg.hex() != payload['message']:
        raise UnexpectedPreimage
    # Does the message signer match the user preimage
    if state_channel.recover(payload) != payload['user']:
        raise UnexpectedSigner
    # Is the preimage value strictly greater than the db value
    db_value = mock_db_connection.execute("""SELECT * FROM tbl;""")
    if payload['value'] <= db_value:
        raise IOUPaymentTooLow
    #  TODO:
    #  (1) Store IOU in db
    #  (2) Set user has_paid state to True (session or db?)
    #  (3) Allow user to play game
    return jsonify(payload)
