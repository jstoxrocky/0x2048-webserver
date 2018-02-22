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
)
from webserver.exceptions import (
    ValidationError,
    IOUPaymentTooLow,
    UnexpectedPayment,
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
    # Ensure user has not already paid
    if session.get('has_paid', False):
        raise UnexpectedPayment
    # Validate payload
    payload = request.get_json()
    if SignatureSchema().validate(payload):
        raise ValidationError
    # Validate IOU
    state_channel.validate_iou(payload)
    # Ensure the preimage value is strictly greater than the db value
    db_value = mock_db_connection.execute("""SELECT * FROM tbl;""")
    if payload['value'] <= db_value:
        raise IOUPaymentTooLow
    #  TODO:
    #  (1) Store IOU in db
    session['has_paid'] = True
    return jsonify(payload)
