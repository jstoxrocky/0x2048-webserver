import json
import io
from webserver.exceptions import (
    ValidationError,
)
from webserver.state_channel import (
    recover,
)
from requests import (
    Response,
)


def test_price(mocker, app, api_prefix, owner, user):
    mocker.patch('webserver.endpoints.price.PRIV', owner.privateKey)
    get = mocker.patch('webserver.price.requests.get')
    response = Response()
    data = {'data': {'amount': 1700}}
    response.raw = io.BytesIO(json.dumps(data).encode())
    get.return_value = response

    # Expected values
    expected_status_code = 200
    expected_outer_subset = {
        'signature', 'price',
    }
    expected_signature_subset = {
        'message', 'messageHash', 'v', 'r', 's', 'signature',
    }
    expected_signer = owner.address

    # Generate Ouput
    query_string = dict(user=user.address)
    endpoint = api_prefix + '/price'
    output = app.get(endpoint, query_string=query_string)
    output_status_code = output.status_code

    # Test
    assert output_status_code == expected_status_code
    output_data = json.loads(output.data)
    ouput_outer_set = set(output_data.keys())
    assert expected_outer_subset <= ouput_outer_set
    output_signature_set = set(output_data['signature'].keys())
    assert expected_signature_subset <= output_signature_set
    signature = output_data['signature']
    output_signer = recover(signature)
    assert expected_signer == output_signer


def test_price_no_address(mocker, app, api_prefix):
    # Mock
    response = Response()
    data = {'data': {'amount': 1700}}
    response.raw = io.BytesIO(json.dumps(data).encode())
    mocker.patch('webserver.price.requests.get')

    # Expected values
    expected_status_code = ValidationError.status_code
    expected_message = ValidationError.message

    # Generate output
    query_string = dict()
    endpoint = api_prefix + '/price'
    output = app.get(endpoint, query_string=query_string)
    output_status_code = output.status_code

    assert output_status_code == expected_status_code
    output_data = json.loads(output.data)
    output_message = output_data['message']
    assert expected_message == output_message
