import json
from webserver.gameplay import (
    new,
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
