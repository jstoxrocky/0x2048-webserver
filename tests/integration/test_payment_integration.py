import json
from webserver.gameplay import (
    new,
)
from webserver.schemas import (
    GamestateSchema,
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
    validate = mocker.patch('webserver.endpoints.iou.IOUSchema.validate')
    validate.return_value = {}
    validate_iou = mocker.patch('webserver.endpoints.iou.state_channel.validate_iou')  # noqa: E501
    validate_iou.return_value = True
    validate_iou = mocker.patch('webserver.endpoints.iou.mock_db_connection.execute')  # noqa: E501
    validate_iou.return_value = 0
    validate = mocker.patch('webserver.endpoints.move.MoveSchema.validate')
    validate.return_value = {}
    next_state = mocker.patch('webserver.endpoints.move.next_state')
    next_state.return_value = new()

    endpoint = api_prefix + '/iou'
    response = app.post(
        endpoint,
        data=json.dumps({'value': 100}),
        content_type='application/json'
    )

    endpoint = api_prefix + '/move'
    response = app.post(
        endpoint,
        data=json.dumps({'user': user.address, 'direction': 1}),
        content_type='application/json'
    )

    output = json.loads(response.data)
    errors = GamestateSchema().validate(output)
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
