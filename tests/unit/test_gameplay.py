from webserver.gameplay import (
    new,
    load,
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
