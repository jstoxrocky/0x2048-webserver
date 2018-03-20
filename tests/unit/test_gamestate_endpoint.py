import json
from webserver.schemas import (
    SignedGamestateSchema,
)
from webserver.config import (
    INITIAL_STATE,
)


def test_gamestate_validates(app, api_prefix):
    endpoint = api_prefix + '/gamestate'
    response = app.get(endpoint)
    output = json.loads(response.data)
    errors = SignedGamestateSchema().validate(output)
    assert not errors


def test_newgame_is_initial_state(app, api_prefix):
    with app as c:
        with c.session_transaction() as sess:
            if sess.get('state'):
                del sess['state']
    endpoint = api_prefix + '/gamestate'
    response = app.get(endpoint)
    output = json.loads(response.data)
    assert output == INITIAL_STATE
