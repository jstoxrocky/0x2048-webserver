import pytest
import fakeredis
import json
from webserver.move import (
    move as post_move,
)
from webserver.schemas import (
    SignedGamestate,
    PaidSession,
)
from webserver.arcade import (
    Arcade,
)
from webserver.exceptions import (
    MoveValidationError,
    PaidSessionValidationError,
)


def test_happy_path(user, mocker):
    # Move
    session_id = Arcade.new_session_id()
    move_payload = {
        'session_id': session_id,
        'direction': 1,
    }

    # PaidSession
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
    redis.set(session_id, json.dumps(paid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Run
    signed_gamestate = json.loads(post_move(move_payload))
    session = json.loads(redis.get(session_id))

    # Test
    errors = SignedGamestate().validate(signed_gamestate)
    assert not errors
    errors = PaidSession().validate(session)
    assert not errors


def test_user_provides_bad_move_payload(user, mocker):
    # Move
    move_payload = {}

    # Run / Test
    with pytest.raises(MoveValidationError):
        post_move(move_payload)


def test_user_has_no_session_id_in_redis(user, mocker):
    # Move
    session_id = Arcade.new_session_id()
    move_payload = {
        'session_id': session_id,
        'direction': 1,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(PaidSessionValidationError):
        post_move(move_payload)


def test_user_has_incorrect_session(user, mocker):
    # Move
    session_id = Arcade.new_session_id()
    move_payload = {
        'session_id': session_id,
        'direction': 1,
    }

    # PaidSession
    paid_session = {}
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(paid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(PaidSessionValidationError):
        post_move(move_payload)
