from webserver.gameplay import (
    new,
    next_state,
)
from webserver.config import (
    INITIAL_STATE,
)
from webserver.schemas import (
    GamestateSchema,
)


def test_new_game():
    output = new()
    errors = GamestateSchema().validate(output)
    assert not errors


def test_next_state():
    state = new()
    direction = 1
    output, gameover = next_state(state, direction)
    errors = GamestateSchema().validate(output)
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
    output, gameover = next_state(state, direction)
    assert gameover
