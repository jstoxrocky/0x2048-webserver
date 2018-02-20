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
    UnexpectedDataFormat,
    UnexpectedDataType,
    MissingUser,
    UnexpectedPreimage,
    UnexpectedSigner,
    IOUPaymentTooLow,
)
from eth_utils import (
    is_checksum_address,
)
from webserver.config import (
    ACCOUNT_ADDR,
)
from webserver import (
    state_channel,
)


blueprint = Blueprint('iou', __name__)
REQUIRED_DATA = {
    'message': str,
    'messageHash': str,
    'v': int,
    'r': str,
    's': str,
    'signature': str,
    'user': str,
    'value': int,
}


class mock_db_connection:
    value = 7

    @classmethod
    def execute(cls, query):
        return cls.value


@blueprint.route('/iou', methods=['POST'])
@cross_origin(origins=ORIGINS, methods=['POST'], supports_credentials=True)
def iou():
    payload = request.get_json()
    # Does the payload dict contain all the required keys
    if not REQUIRED_DATA.keys() <= payload.keys():
        raise UnexpectedDataFormat
    # Does the payload data types match what we are expecting
    for key, value in payload.items():
        if not isinstance(value, REQUIRED_DATA[key]):
            raise UnexpectedDataType
    # Does the user address pass a checksum
    if not is_checksum_address(payload['user']):
        raise MissingUser
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
    return jsonify(payload)
