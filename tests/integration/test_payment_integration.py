import json
from webserver.endpoints.iou import (
    mock_db_connection,
)
from webserver import (
    state_channel,
)
from webserver.config import (
    ACCOUNT_ADDR,
)
from toolz.dicttoolz import (
    merge,
)


def test_pay_and_move(mocker, app, api_prefix, owner, user, new_game):
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

    # Pay
    value = mock_db_connection.value + 1
    msg = state_channel.solidity_keccak(ACCOUNT_ADDR, user.address, value)
    signed = state_channel.sign(msg, user.privateKey)
    payload = merge(signed, {'user': user.address, 'value': value})
    data = payload
    json_data = json.dumps(data)
    endpoint = api_prefix + '/iou'
    app.post(
        endpoint,
        data=json_data,
        content_type='application/json'
    )
    with app as c:
        with c.session_transaction() as sess:
            assert sess['has_paid']

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
    output_signer = state_channel.recover(signature)
    assert expected_signer == output_signer
