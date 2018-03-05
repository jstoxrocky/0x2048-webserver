import json
from webserver.schemas import (
    GamestateSchema,
)
from webserver.config import (
    INITIAL_STATE,
)


def test_gamestate_validates(app, api_prefix):
    endpoint = api_prefix + '/gamestate'
    response = app.get(endpoint)
    output = json.loads(response.data)
    errors = GamestateSchema().validate(output)
    assert not errors


def test_newgame_validates(app, api_prefix):
    endpoint = api_prefix + '/gamestate'
    response = app.get(endpoint)
    output = json.loads(response.data)
    errors = GamestateSchema().validate(output)
    assert not errors


def test_newgame_is_initial_state(app, api_prefix):
    endpoint = api_prefix + '/gamestate'
    response = app.get(endpoint)
    output = json.loads(response.data)
    assert output == INITIAL_STATE
