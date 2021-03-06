import json
import fakeredis
from app import (
    app as application,
)


ADDRESS = '0x0A34371d4BB7c49Ec9e4c156b525eA7417f63e7A'


def test_payment_code_happy_path(mocker):
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch(
        'webserver.payment_code.redis.Redis.from_url',
    ).return_value = redis

    app = application.test_client()
    app.testing = True
    data = {}
    response = app.get(
        '/api/v1/payment_code',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200


def test_confirm_payment_happy_path(mocker, user, monkeypatch):
    app = application.test_client()
    app.testing = True
    session_id = '0x5dc99a053b9a2ca01da214a3a159e4c2da7be0ba7ff4e073551e023e31c5a332'  # noqa: E501
    payment_code = '0x1c3103ad99a02bea73d377c82a490eef72fea445b39a2ec8e4b6e671b534b13b'  # noqa: E501
    payload = {
        'session_id': session_id,
        'user': user.address,
    }

    # Session
    unpaid_session = {
        'paid': False,
        'payment_code': payment_code,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch(
        'webserver.payment_confirmation.redis.Redis.from_url',
    ).return_value = redis

    # Contract
    monkeypatch.setattr("webserver.payment_confirmation.ADDRESS", ADDRESS)
    contract = mocker.patch(
        'webserver.payment_confirmation.arcade_protocol.Contract',
    ).return_value
    contract.get_payment_code.return_value = payment_code
    contract.address = ADDRESS
    contract.game_id = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4e'   # noqa: E501

    response = app.get(
        '/api/v1/payment_confirmation',
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
    paid_session = {
        'paid': True,
        'gamestate': gamestate,
        'user': user.address,
    }

    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(paid_session))
    mocker.patch('webserver.move.redis.Redis.from_url').return_value = redis

    response = app.post(
        '/api/v1/move',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200


def test_metadata_happy_path(mocker, mock_contract):
    mocker.patch('webserver.metadata.ethusd.fetch_exchange_rate').return_value = 200.00   # noqa: E501
    mocker.patch('webserver.metadata.contract.arcade_contract').return_value = mock_contract   # noqa: E501

    app = application.test_client()
    app.testing = True
    data = {}
    response = app.get(
        '/api/v1/metadata',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200
