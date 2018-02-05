import json
import io
from webserver.exceptions import (
    UnknownMove,
    MissingUser,
)
from eth_utils import (
    decode_hex,
)
from web3 import (
    Account,
)
from unittest.mock import (
    patch,
)
from requests import (
    Response,
)


def recover(message, signature):
    return Account.recoverMessage(
        data=decode_hex(message),
        signature=decode_hex(signature),
    )


@patch('webserver.price.requests.get')
def test_price(mocked, app, owner, user):
    # Mock
    response = Response()
    data = {'data': {'amount': 1700}}
    response.raw = io.BytesIO(json.dumps(data).encode())
    mocked.return_value = response

    # Expected values
    expected_status_code = 200
    expected_outer_subset = {
        'signature', 'price',
    }
    expected_signature_subset = {
        'message', 'messageHash', 'v', 'r', 's', 'signature',
    }
    expected_signer = owner

    # Generate Ouput
    query_string = dict(user=user)
    output = app.get('/price', query_string=query_string)
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


@patch('webserver.price.requests.get')
def test_price_no_address(mocked, app):
    # Mock
    response = Response()
    data = {'data': {'amount': 1700}}
    response.raw = io.BytesIO(json.dumps(data).encode())
    mocked.return_value = response

    # Expected values
    expected_status_code = MissingUser.status_code
    expected_message = MissingUser.message

    # Generate output
    query_string = dict()
    output = app.get('/price', query_string=query_string)
    output_status_code = output.status_code

    assert output_status_code == expected_status_code
    output_data = json.loads(output.data)
    output_message = output_data['message']
    assert expected_message == output_message


def test_move(app, owner, user, new_game):
    # Expected values
    expected_status_code = 200
    expected_outer_subset = {
        'signature', 'score', 'board', 'gameover',
    }
    expected_signature_subset = {
        'message', 'messageHash', 'v', 'r', 's', 'signature',
    }
    expected_signer = owner

    # Generate Ouput
    data = json.dumps(dict(direction=1, user=user))
    output = app.post('/move', data=data, content_type='application/json')
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


def test_move_no_address(app):
    # Expected values
    expected_status_code = MissingUser.status_code
    expected_message = MissingUser.message

    # Generate output
    data = json.dumps(dict(direction=1))
    output = app.post('/move', data=data, content_type='application/json')
    output_status_code = output.status_code

    # Test
    assert output_status_code == expected_status_code
    output = json.loads(output.data)
    output_message = output['message']
    assert expected_message == output_message


def test_move_no_move(app, user, new_game):
    # Expected values
    expected_status_code = UnknownMove.status_code
    expected_message = UnknownMove.message

    # Generate output
    data = json.dumps(dict(user=user))
    output = app.post('/move', data=data, content_type='application/json')
    output_status_code = output.status_code

    # Test
    assert output_status_code == expected_status_code
    output = json.loads(output.data)
    output_message = output['message']
    assert expected_message == output_message
