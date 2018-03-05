import json
from webserver.exceptions import (
    ValidationError,
    UnexpectedSignature,
    IOUPaymentTooLow,
    UnexpectedPayment,
)
from webserver.schemas import (
    SignedGamestateSchema,
)


def test_has_already_paid(app, api_prefix, session_has_paid):
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json.dumps({}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    assert response.status_code == UnexpectedPayment.status_code
    assert output['message'] == UnexpectedPayment.message


def test_validation_error(mocker, app, api_prefix, session_has_not_paid):
    validate = mocker.patch('webserver.endpoints.iou.IOUSchema.validate')
    validate.return_value = {'error_key': ['error_message']}
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json.dumps({}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    assert response.status_code == ValidationError.status_code
    assert output['message'] == ValidationError.message


def test_signature_error(mocker, app, api_prefix, session_has_not_paid):
    validate = mocker.patch('webserver.endpoints.iou.IOUSchema.validate')
    validate.return_value = {}
    validate_iou = mocker.patch('webserver.endpoints.iou.state_channel.validate_iou')  # noqa: E501
    validate_iou.return_value = False
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json.dumps({}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    assert response.status_code == UnexpectedSignature.status_code
    assert output['message'] == UnexpectedSignature.message


def test_payment_error(mocker, app, api_prefix, session_has_not_paid):
    validate = mocker.patch('webserver.endpoints.iou.IOUSchema.validate')
    validate.return_value = {}
    validate_iou = mocker.patch('webserver.endpoints.iou.state_channel.validate_iou')  # noqa: E501
    validate_iou.return_value = True
    execute = mocker.patch('webserver.endpoints.iou.mock_db_connection.execute')  # noqa: E501
    execute.return_value = 100
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json.dumps({'value': 1}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    assert response.status_code == IOUPaymentTooLow.status_code
    assert output['message'] == IOUPaymentTooLow.message


def test_success(mocker, app, api_prefix, user, session_has_not_paid):
    validate = mocker.patch('webserver.endpoints.iou.IOUSchema.validate')
    validate.return_value = {}
    validate_iou = mocker.patch('webserver.endpoints.iou.state_channel.validate_iou')  # noqa: E501
    validate_iou.return_value = True
    execute = mocker.patch('webserver.endpoints.iou.mock_db_connection.execute')  # noqa: E501
    execute.return_value = 0
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json.dumps({'value': 100, 'user': user.address}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    errors = SignedGamestateSchema().validate(output)
    assert not errors
    with app as c:
        with c.session_transaction() as sess:
            assert sess['has_paid']


def test_nonce_validation_error(mocker, app, api_prefix, user):
    validate = mocker.patch('webserver.endpoints.iou.UserSchema.validate')
    validate.return_value = {'error_key': ['error_message']}
    endpoint = api_prefix + '/nonce'
    response = app.get(
        endpoint,
        query_string={},
    )
    output = json.loads(response.data)
    assert response.status_code == ValidationError.status_code
    assert output['message'] == ValidationError.message


def test_nonce_success(mocker, app, api_prefix, user):
    validate_iou = mocker.patch('webserver.endpoints.iou.mock_db_connection.execute')  # noqa: E501
    validate_iou.return_value = 17
    endpoint = api_prefix + '/nonce'
    response = app.get(
        endpoint,
        query_string={'user': user.address},
    )
    output = json.loads(response.data)
    assert output == {'value': 17}
