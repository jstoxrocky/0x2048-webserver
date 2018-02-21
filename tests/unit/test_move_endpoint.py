import json
from webserver.exceptions import (
    ValidationError,
    PaymentRequired,
)
from webserver.state_channel import (
    recover,
)


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
    # Set has paid to True
    with app as c:
        with c.session_transaction() as sess:
            sess['has_paid'] = True

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
    output_signer = recover(signature)
    assert expected_signer == output_signer


def test_move_no_pay(app, api_prefix, user):
    # Expected values
    expected_status_code = PaymentRequired.status_code
    expected_message = PaymentRequired.message

    # Set has paid to False
    with app as c:
        with c.session_transaction() as sess:
            sess['has_paid'] = False

    # Generate output
    data = json.dumps(dict(direction=1, user=user.address))
    endpoint = api_prefix + '/move'
    output = app.post(endpoint, data=data, content_type='application/json')
    output_status_code = output.status_code

    # Test
    assert output_status_code == expected_status_code
    output = json.loads(output.data)
    output_message = output['message']
    assert expected_message == output_message


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
