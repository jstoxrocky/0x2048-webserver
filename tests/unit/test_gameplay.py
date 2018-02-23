from webserver.gameplay import (
    new,
    load,
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
    output = load(state, direction)
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
    output = load(state, direction)
    assert output['gameover']


def test_next_state_gameover(mocker):
    new = mocker.patch('webserver.gameplay.new')
    new.return_value = True
    state = {}
    direction = 0
    gameover = True
    success = next_state(state, direction, gameover)
    assert success


def test_next_state_not_gameover(mocker):
    load = mocker.patch('webserver.gameplay.load')
    load.return_value = True
    state = {}
    direction = 0
    gameover = False
    success = next_state(state, direction, gameover)
    assert success
