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
    UnexpectedSignature,
)
from webserver import (
    state_channel,
)
from webserver.schemas import (
    IOUSchema,
    UserSchema,
)


blueprint = Blueprint('iou', __name__)


class mock_db_connection:
    value = 7

    @classmethod
    def execute(cls, query):
        return cls.value


@blueprint.route('/iou', methods=['GET', 'POST'])
@cross_origin(origins=ORIGINS, methods=['GET', 'POST'],
              supports_credentials=True)
def iou():
    if request.method == 'GET':
        # Validate payload
        payload = request.args
        if UserSchema().validate(payload):
            raise ValidationError
        # Get most recent value
        db_value = mock_db_connection.execute("""SELECT * FROM tbl;""")
        return jsonify({'value': db_value})
    elif request.method == 'POST':
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
        #  TODO:
        #  (1) Store IOU in db
        session['has_paid'] = True
        return jsonify({'success': True})
