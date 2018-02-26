import json
from webserver.schemas import (
    GamestateSchema,
)


def test_validates(app, api_prefix):
    endpoint = api_prefix + '/gamestate'
    response = app.get(endpoint)
    output = json.loads(response.data)
    errors = GamestateSchema().validate(output)
    assert not errors
