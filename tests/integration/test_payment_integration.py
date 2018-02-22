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


def test_pay_and_move(mocker, app, api_prefix,
                      owner, user, session_has_not_paid):
    mocker.patch('webserver.endpoints.move.PRIV', owner.privateKey)
    # Expected values
    expected_status_code = 200

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


def test_move_gameover_has_paid(app, api_prefix,
                                owner, user, session_has_paid):
    """
    It should revert session['has_paid'] to False on gameover
    """
    with app as c:
        with c.session_transaction() as sess:
            sess['state']['board'] = [
                [8, 16, 8, 0],
                [16, 8, 16, 8],
                [8, 16, 8, 16],
                [16, 8, 16, 8],
            ]

    # Generate Ouput
    data = json.dumps(dict(direction=1, user=user.address))
    endpoint = api_prefix + '/move'
    app.post(endpoint, data=data, content_type='application/json')

    with app as c:
        with c.session_transaction() as sess:
            assert not sess['has_paid']
