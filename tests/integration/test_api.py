import json
import fakeredis
from app import (
    app as application,
)
from webserver.game_config import (
    TWENTY_FORTY_EIGHT,
)


def test_payment_code_happy_path():
    app = application.test_client()
    app.testing = True
    data = {}
    response = app.get(
        '/api/v1/payment_code',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200


def test_game_happy_path(mocker, user):
    app = application.test_client()
    app.testing = True
    session_id = '0x5dc99a053b9a2ca01da214a3a159e4c2da7be0ba7ff4e073551e023e31c5a332'  # noqa: E501
    payment_code = '0x1c3103ad99a02bea73d377c82a490eef72fea445b39a2ec8e4b6e671b534b13b'  # noqa: E501
    game_id = TWENTY_FORTY_EIGHT
    payload = {
        'session_id': session_id,
        'address': user.address,
        'game_id': game_id,
    }

    # Session
    unpaid_session = {
        'paid': False,
        'payment_code': payment_code,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getPaymentCode.return_value \
        .call.return_value = payment_code

    response = app.get(
        '/api/v1/game',
        query_string=payload,
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
    game_id = TWENTY_FORTY_EIGHT
    paid_session = {
        'paid': True,
        'gamestate': gamestate,
        'address': user.address,
        'game_id': game_id,
    }

    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(paid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    response = app.post(
        '/api/v1/move',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200


def test_game_info_happy_path(mocker):
    app = application.test_client()
    app.testing = True

    highscore = 1000
    jackpot = 100
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getHighscore.return_value \
        .call.return_value = highscore
    contract.functions.getJackpot.return_value \
        .call.return_value = jackpot

    response = app.get(
        '/api/v1/game_info',
        content_type='application/json'
    )
    assert response.status_code == 200
