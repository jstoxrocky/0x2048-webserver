import pytest
import json
from webserver.exceptions import (
    ValidationError,
    UnexpectedPreimage,
    UnexpectedSigner,
    IOUPaymentTooLow,
)
from toolz.dicttoolz import (
    merge,
)
from webserver import (
    state_channel,
)
from webserver.config import (
    ACCOUNT_ADDR,
)
from webserver.endpoints.iou import (
    mock_db_connection,
)


DEFAULT_DATA = {
    'message': '0x00',
    'messageHash': '0x00',
    'v': 27,
    'r': '0x00',
    's': '0x00',
    'signature': '0x00',
    'user': '0x00',
    'value': 1,
}


def test_bad_data(app, api_prefix):
    """
    It should raise a ValidationError exception
    """
    # Expected values
    expected_status_code = ValidationError.status_code
    expected_message = ValidationError.message

    data = {'x': 17}
    json_data = json.dumps(data)
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json_data,
        content_type='application/json'
    )

    # Test
    assert response.status_code == expected_status_code
    output = json.loads(response.data)
    output_message = output['message']
    assert expected_message == output_message


@pytest.mark.parametrize('key,value', [
    ('message', 0),
    ('messageHash', 0),
    ('v', ''),
    ('r', 0),
    ('s', 0),
    ('signature', 0),
    ('user', 0),
    ('value', ''),
])
def test_bad_types(app, api_prefix, key, value):
    """
    It should raise a ValidationError exception
    """
    # Expected values
    expected_status_code = ValidationError.status_code
    expected_message = ValidationError.message

    data = merge(DEFAULT_DATA, {key: value})
    json_data = json.dumps(data)
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json_data,
        content_type='application/json'
    )

    # Test
    assert response.status_code == expected_status_code
    output = json.loads(response.data)
    output_message = output['message']
    assert expected_message == output_message


@pytest.mark.parametrize('test_user,test_value', [
    (None, 1337),
    ('0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69', None)  # user2.address
])
def test_bad_preimage(app, api_prefix, user, test_user, test_value):
    """
    It should raise UnexpectedPreimage exception
    """
    value = 1
    if not test_user:
        test_user = user.address
    if not test_value:
        test_value = value

    # Expected values
    expected_status_code = UnexpectedPreimage.status_code
    expected_message = UnexpectedPreimage.message

    msg = state_channel.solidityKeccak(ACCOUNT_ADDR, user.address, value)
    signed = state_channel.sign(msg, user.privateKey)
    payload = merge(signed, {'user': test_user, 'value': test_value})
    data = payload
    json_data = json.dumps(data)
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json_data,
        content_type='application/json'
    )

    # Test
    assert response.status_code == expected_status_code
    output = json.loads(response.data)
    output_message = output['message']
    assert expected_message == output_message


def test_bad_signer(app, api_prefix, user, user2):
    """
    It should raise UnexpectedSigner exception
    """
    value = 1

    # Expected values
    expected_status_code = UnexpectedSigner.status_code
    expected_message = UnexpectedSigner.message

    msg = state_channel.solidityKeccak(ACCOUNT_ADDR, user.address, value)
    signed = state_channel.sign(msg, user2.privateKey)
    payload = merge(signed, {'user': user.address, 'value': value})
    data = payload
    json_data = json.dumps(data)
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json_data,
        content_type='application/json'
    )

    # Test
    assert response.status_code == expected_status_code
    output = json.loads(response.data)
    output_message = output['message']
    assert expected_message == output_message


def test_value_too_low(app, api_prefix, user, user2):
    """
    It should raise IOUPaymentTooLow exception
    """
    value = mock_db_connection.value

    # Expected values
    expected_status_code = IOUPaymentTooLow.status_code
    expected_message = IOUPaymentTooLow.message

    msg = state_channel.solidityKeccak(ACCOUNT_ADDR, user.address, value)
    signed = state_channel.sign(msg, user.privateKey)
    payload = merge(signed, {'user': user.address, 'value': value})
    data = payload
    json_data = json.dumps(data)
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json_data,
        content_type='application/json'
    )

    # Test
    assert response.status_code == expected_status_code
    output = json.loads(response.data)
    output_message = output['message']
    assert expected_message == output_message


def test_iou_endpoint(app, api_prefix, user):
    """
    It should return the same data sent to it
    """
    value = mock_db_connection.value + 1
    msg = state_channel.solidityKeccak(ACCOUNT_ADDR, user.address, value)
    signed = state_channel.sign(msg, user.privateKey)
    payload = merge(signed, {'user': user.address, 'value': value})
    data = payload
    json_data = json.dumps(data)
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json_data,
        content_type='application/json'
    )
    output = json.loads(response.data)
    assert output == data
