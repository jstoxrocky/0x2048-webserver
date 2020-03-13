import json
import fakeredis
from web3 import (
    Account,
)
from hexbytes import (
    HexBytes,
)
from webserver.application import (
    application,
)
from webserver.signing import (
    prepare_structured_nonce_for_signing
)


def test_new_session_happy_path():
    app = application.test_client()
    app.testing = True
    data = {}
    response = app.get(
        '/new_session',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200


def test_new_game_happy_path(mocker, user):
    app = application.test_client()
    app.testing = True
    session_id = '0x5dc99a053b9a2ca01da214a3a159e4c2da7be0ba7ff4e073551e023e31c5a332'  # noqa: E501
    challenge = '0x1c3103ad99a02bea73d377c82a490eef72fea445b39a2ec8e4b6e671b534b13b'  # noqa: E501

    # Challenge
    signable_message = prepare_structured_nonce_for_signing(
        challenge
    )
    signature = Account.sign_message(signable_message, user.key)
    data = {
        'session_id': session_id,
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }

    # Session
    unpaid_session = {
        'paid': False,
        'challenge': challenge,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value \
        .call.return_value = challenge

    response = app.post(
        '/new_game',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200


def test_move_happy_path(mocker, user):
    app = application.test_client()
    app.testing = True
    session_id = '0x5dc99a053b9a2ca01da214a3a159e4c2da7be0ba7ff4e073551e023e31c5a332'  # noqa: E501

    # Move
    data = {
        'session_id': session_id,
        'direction': 1,
    }

    # Session
    gamestate = {
        'board': [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 0, 0]
        ],
        'score': 0,
        'gameover': False,
    }
    paid_session = {
        'paid': True,
        'gamestate': gamestate,
        'recovered_address': user.address,
    }

    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(paid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    response = app.post(
        '/move',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200
