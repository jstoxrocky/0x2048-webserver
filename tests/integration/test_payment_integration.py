import json
from webserver.gameplay import (
    new,
)
from webserver.schemas import (
    SignedGamestateSchema,
)
from webserver.state_channel import (
    recover,
)
from webserver.config import (
    PRIV,
)
from web3 import (
    Account,
)


def test_pay_and_move(mocker, app, api_prefix, user, session_has_not_paid):
    validate_iou_schema = mocker.patch('webserver.endpoints.iou.IOUSchema.validate')  # noqa: E501
    validate_iou_schema.return_value = {}
    validate_iou = mocker.patch('webserver.endpoints.iou.state_channel.validate_iou')  # noqa: E501
    validate_iou.return_value = True
    get_latest_nonce = mocker.patch('webserver.endpoints.iou.get_latest_nonce')
    get_latest_nonce.return_value = 0
    get_latest_nonce = mocker.patch('webserver.endpoints.iou.insert_iou')
    get_latest_nonce.return_value = True
    calc_net_time_left = mocker.patch('webserver.endpoints.iou.calc_net_time_left')  # noqa: E501
    calc_net_time_left.return_value = 1
    calc_net_balance = mocker.patch('webserver.endpoints.iou.calc_net_balance')
    calc_net_balance.return_value = 1
    validate_move_schema = mocker.patch('webserver.endpoints.move.MoveSchema.validate')  # noqa: E501
    validate_move_schema.return_value = {}
    next_state = mocker.patch('webserver.endpoints.move.next_state')
    next_state.return_value = new()
    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json.dumps({'nonce': 100, 'user': user.address}),
        content_type='application/json'
    )
    endpoint = api_prefix + '/move'
    response = app.post(
        endpoint,
        data=json.dumps({'user': user.address, 'direction': 1}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    errors = SignedGamestateSchema().validate(output)
    assert not errors


def test_signer_is_envvar(mocker, app, api_prefix, user, session_has_paid):
    validate = mocker.patch('webserver.endpoints.move.MoveSchema.validate')
    validate.return_value = {}
    next_state = mocker.patch('webserver.endpoints.move.next_state')
    next_state.return_value = new()
    endpoint = api_prefix + '/move'
    response = app.post(
        endpoint,
        data=json.dumps({'user': user.address, 'direction': 1}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    signed = output['signature']
    signer = recover(
        signed['messageHash'],
        signed['signature'],
    )
    owner = Account.privateKeyToAccount(PRIV).address
    assert signer == owner
