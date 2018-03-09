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
    validate_schema = mocker.patch('webserver.endpoints.iou.IOUSchema.validate')  # noqa: E501
    validate_schema.return_value = {'error_key': ['error_message']}
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
    validate_schema = mocker.patch('webserver.endpoints.iou.IOUSchema.validate')  # noqa: E501
    validate_schema.return_value = {}
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


def test_payment_error(mocker, app, api_prefix, user, session_has_not_paid):
    validate_schema = mocker.patch('webserver.endpoints.iou.IOUSchema.validate')  # noqa: E501
    validate_schema.return_value = {}
    validate_iou = mocker.patch('webserver.endpoints.iou.state_channel.validate_iou')  # noqa: E501
    validate_iou.return_value = True
    get_latest_nonce = mocker.patch('webserver.endpoints.iou.get_latest_nonce')
    get_latest_nonce.return_value = 100
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json.dumps({'nonce': 1, 'user': user.address}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    assert response.status_code == IOUPaymentTooLow.status_code
    assert output['message'] == IOUPaymentTooLow.message


def test_iou_success(mocker, app, api_prefix, user, session_has_not_paid):
    validate_schema = mocker.patch('webserver.endpoints.iou.IOUSchema.validate')  # noqa: E501
    validate_schema.return_value = {}
    validate_iou = mocker.patch('webserver.endpoints.iou.state_channel.validate_iou')  # noqa: E501
    validate_iou.return_value = True
    get_latest_nonce = mocker.patch('webserver.endpoints.iou.get_latest_nonce')
    get_latest_nonce.return_value = 0
    insert_iou = mocker.patch('webserver.endpoints.iou.insert_iou')
    insert_iou.return_value = True
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json.dumps({'nonce': 100, 'user': user.address}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    errors = SignedGamestateSchema().validate(output)
    assert not errors
    with app as c:
        with c.session_transaction() as sess:
            assert sess['has_paid']


def test_nonce_validation_error(mocker, app, api_prefix, user):
    validate_schema = mocker.patch('webserver.endpoints.iou.UserSchema.validate')  # noqa: E501
    validate_schema.return_value = {'error_key': ['error_message']}
    endpoint = api_prefix + '/nonce'
    response = app.get(
        endpoint,
        query_string={},
    )
    output = json.loads(response.data)
    assert response.status_code == ValidationError.status_code
    assert output['message'] == ValidationError.message


def test_nonce_success(mocker, app, api_prefix, user):
    nonce = 17
    get_latest_nonce = mocker.patch('webserver.endpoints.iou.get_latest_nonce')
    get_latest_nonce.return_value = nonce
    endpoint = api_prefix + '/nonce'
    response = app.get(
        endpoint,
        query_string={'user': user.address},
    )
    output = json.loads(response.data)
    assert output == {'nonce': nonce}
