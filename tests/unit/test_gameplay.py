from webserver.gameplay import (
    new,
    next_state,
)
from webserver.config import (
    INITIAL_STATE,
)
from webserver import schemas


def test_new_game():
    output = new()
    errors = schemas.Gamestate().validate(output)
    assert not errors


def test_next_state():
    state = new()
    direction = 1
    output = next_state(state, direction)
    errors = schemas.Gamestate().validate(output)
    assert not errors


def test_gameover():
    board = [
        [8, 16, 8, 0],
        [16, 8, 16, 8],
        [8, 16, 8, 16],
        [16, 8, 16, 8],
    ]
    state = INITIAL_STATE
    state['board'] = board
    direction = 1  # Up
    output = next_state(state, direction)
    assert output['gameover']
