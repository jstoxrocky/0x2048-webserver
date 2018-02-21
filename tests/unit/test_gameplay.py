from webserver.gameplay import (
    new,
    next_state,
)
from webserver.config import (
    INITIAL_STATE,
)


def test_new_game():
    expected_keys = {'score', 'board', 'gameover'}
    output = new()
    assert expected_keys <= set(output.keys())
    assert output['score'] == 0
    assert not output['gameover']


def test_load():
    expected_keys = {'score', 'board', 'gameover'}
    state = new()
    direction = 1
    output = next_state(state, direction)
    assert expected_keys <= set(output.keys())
    assert not output['gameover']


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
