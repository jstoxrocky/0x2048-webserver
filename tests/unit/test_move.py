import pytest
import fakeredis
import json
from webserver.move import (
    move,
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
    arcade_response = Arcade.new_session()
    move_payload = {
        'session_id': arcade_response['session_id'],
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
        'recovered_address': user.address,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(arcade_response['session_id'], json.dumps(paid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Run
    event, context = move_payload, None
    signed_gamestate = json.loads(move(event, context))
    session = json.loads(redis.get(arcade_response['session_id']))

    # Test
    errors = SignedGamestate().validate(signed_gamestate)
    assert not errors
    errors = PaidSession().validate(session)
    assert not errors


def test_user_provides_bad_move_payload(user, mocker):
    # Move
    move_payload = {}

    # Run / Test
    event, context = move_payload, None
    with pytest.raises(MoveValidationError):
        move(event, context)


def test_user_has_no_session_id_in_redis(user, mocker):
    # Move
    arcade_response = Arcade.new_session()
    move_payload = {
        'session_id': arcade_response['session_id'],
        'direction': 1,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Run / Test
    event, context = move_payload, None
    with pytest.raises(PaidSessionValidationError):
        move(event, context)


def test_user_has_incorrect_session(user, mocker):
    # Move
    arcade_response = Arcade.new_session()
    move_payload = {
        'session_id': arcade_response['session_id'],
        'direction': 1,
    }

    # PaidSession
    paid_session = {}
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(arcade_response['session_id'], json.dumps(paid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Run / Test
    event, context = move_payload, None
    with pytest.raises(PaidSessionValidationError):
        move(event, context)
