import json
import fakeredis
from web3 import (
    Account,
)
from hexbytes import (
    HexBytes,
)
from app import (
    app as application,
)
from webserver.signing import (
    prepare_structured_gamecode_for_signing
)


def test_gamecode_happy_path():
    app = application.test_client()
    app.testing = True
    data = {}
    response = app.get(
        '/api/v1/gamecode',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200


def test_new_game_happy_path(mocker, user):
    app = application.test_client()
    app.testing = True
    gamecode = '0x5dc99a053b9a2ca01da214a3a159e4c2da7be0ba7ff4e073551e023e31c5a332'  # noqa: E501

    signable_message = prepare_structured_gamecode_for_signing(
        gamecode,
    )
    signature = Account.sign_message(signable_message, user.key)
    data = {
        'gamecode': gamecode,
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }

    # Session
    unpaid_session = {
        'paid': False,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(gamecode, json.dumps(unpaid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value \
        .call.return_value = gamecode

    response = app.post(
        '/api/v1/new_game',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200


def test_move_happy_path(mocker, user):
    app = application.test_client()
    app.testing = True
    gamecode = '0x5dc99a053b9a2ca01da214a3a159e4c2da7be0ba7ff4e073551e023e31c5a332'  # noqa: E501

    # Move
    data = {
        'gamecode': gamecode,
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
        'address': user.address,
    }

    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(gamecode, json.dumps(paid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    response = app.post(
        '/api/v1/move',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200
