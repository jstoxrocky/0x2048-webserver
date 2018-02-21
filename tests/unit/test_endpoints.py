import json
import io
from webserver.exceptions import (
    ValidationError,
)
from eth_utils import (
    decode_hex,
)
from web3 import (
    Account,
)
from requests import (
    Response,
)


def recover(message, signature):
    return Account.recoverMessage(
        data=decode_hex(message),
        signature=decode_hex(signature),
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
    output_signer = recover(signature['message'], signature['signature'])
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


def test_gamestate(app, api_prefix):
    # Expected values
    expected_status_code = 200
    expected_outer_subset = {
        'signature', 'score', 'board', 'gameover',
    }
    expected_signature_subset = {
        'message', 'messageHash', 'v', 'r', 's', 'signature',
    }

    # Generate Ouput
    endpoint = api_prefix + '/gamestate'
    output = app.get(endpoint)
    output_status_code = output.status_code

    # Test
    assert output_status_code == expected_status_code
    output_data = json.loads(output.data)
    ouput_outer_set = set(output_data.keys())
    assert expected_outer_subset <= ouput_outer_set
    output_signature_set = set(output_data['signature'].keys())
    assert expected_signature_subset <= output_signature_set


def test_move(mocker, app, api_prefix, owner, user, new_game):
    mocker.patch('webserver.endpoints.move.PRIV', owner.privateKey)
    # Expected values
    expected_status_code = 200
    expected_outer_subset = {
        'signature', 'score', 'board', 'gameover',
    }
    expected_signature_subset = {
        'message', 'messageHash', 'v', 'r', 's', 'signature',
    }
    expected_signer = owner.address

    # Generate Ouput
    data = json.dumps(dict(direction=1, user=user.address))
    endpoint = api_prefix + '/move'
    output = app.post(endpoint, data=data, content_type='application/json')
    output_status_code = output.status_code

    # Test
    assert output_status_code == expected_status_code
    output_data = json.loads(output.data)
    ouput_outer_set = set(output_data.keys())
    assert expected_outer_subset <= ouput_outer_set
    output_signature_set = set(output_data['signature'].keys())
    assert expected_signature_subset <= output_signature_set
    signature = output_data['signature']
    output_signer = recover(signature['message'], signature['signature'])
    assert expected_signer == output_signer


def test_move_no_address(app, api_prefix):
    # Expected values
    expected_status_code = ValidationError.status_code
    expected_message = ValidationError.message

    # Generate output
    data = json.dumps(dict(direction=1))
    endpoint = api_prefix + '/move'
    output = app.post(endpoint, data=data, content_type='application/json')
    output_status_code = output.status_code

    # Test
    assert output_status_code == expected_status_code
    output = json.loads(output.data)
    output_message = output['message']
    assert expected_message == output_message


def test_move_no_direction(app, api_prefix, user, new_game):
    # Expected values
    expected_status_code = ValidationError.status_code
    expected_message = ValidationError.message

    # Generate output
    data = json.dumps(dict(user=user.address))
    endpoint = api_prefix + '/move'
    output = app.post(endpoint, data=data, content_type='application/json')
    output_status_code = output.status_code

    # Test
    assert output_status_code == expected_status_code
    output = json.loads(output.data)
    output_message = output['message']
    assert expected_message == output_message
