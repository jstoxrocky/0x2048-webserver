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
    gamecode = Arcade.new_gamecode()
    move_payload = {
        'gamecode': gamecode,
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
    redis.set(gamecode, json.dumps(paid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Run
    signed_gamestate = json.loads(move(move_payload))
    session = json.loads(redis.get(gamecode))

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
        move(move_payload)


def test_user_has_no_gamecode_in_redis(user, mocker):
    # Move
    gamecode = Arcade.new_gamecode()
    move_payload = {
        'gamecode': gamecode,
        'direction': 1,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(PaidSessionValidationError):
        move(move_payload)


def test_user_has_incorrect_session(user, mocker):
    # Move
    gamecode = Arcade.new_gamecode()
    move_payload = {
        'gamecode': gamecode,
        'direction': 1,
    }

    # PaidSession
    paid_session = {}
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(gamecode, json.dumps(paid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(PaidSessionValidationError):
        move(move_payload)
