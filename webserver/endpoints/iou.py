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
    # Validate IOU
    state_channel.validate_iou(payload)
    # Is the preimage value strictly greater than the db value
    db_value = mock_db_connection.execute("""SELECT * FROM tbl;""")
    if payload['value'] <= db_value:
        raise IOUPaymentTooLow
    #  TODO:
    #  (1) Store IOU in db
    # Set user has_paid state to True (session or db?)
    session['has_paid'] = True
    return jsonify(payload)
