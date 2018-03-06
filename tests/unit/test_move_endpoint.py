import json
from webserver.exceptions import (
    ValidationError,
    PaymentRequired,
)
from webserver.gameplay import (
    new,
)
from webserver.schemas import (
    GamestateSchema,
)
from webserver.config import (
    INITIAL_STATE,
)


def test_has_not_already_paid(app, api_prefix, session_has_not_paid):
    endpoint = api_prefix + '/move'
    response = app.post(
        endpoint,
        data=json.dumps({}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    assert response.status_code == PaymentRequired.status_code
    assert output['message'] == PaymentRequired.message


def test_validation_error(mocker, app, api_prefix, session_has_paid):
    validate = mocker.patch('webserver.endpoints.move.MoveSchema.validate')
    validate.return_value = {'error_key': ['error_message']}
    endpoint = api_prefix + '/move'
    response = app.post(
        endpoint,
        data=json.dumps({}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    assert response.status_code == ValidationError.status_code
    assert output['message'] == ValidationError.message


def test_validates(mocker, app, api_prefix, user, session_has_paid):
    validate = mocker.patch('webserver.endpoints.move.MoveSchema.validate')
    validate.return_value = {}
    next_state = mocker.patch('webserver.endpoints.move.next_state')
    next_state.return_value = new()
    endpoint = api_prefix + '/move'
    response = app.post(
        endpoint,
        data=json.dumps({'user': user.address, 'direction': 1}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    errors = GamestateSchema().validate(output)
    assert not errors
    with app as c:
        with c.session_transaction() as sess:
            assert sess['has_paid']
            assert not sess['state']['gameover']


def test_gameover(mocker, app, api_prefix, user, session_has_paid):
    validate = mocker.patch('webserver.endpoints.move.MoveSchema.validate')
    validate.return_value = {}
    with app as c:
        with c.session_transaction() as sess:
            sess['state'] = INITIAL_STATE
            sess['state']['board'] = [
                [8, 16, 8, 0],
                [16, 8, 16, 8],
                [8, 16, 8, 16],
                [16, 8, 16, 8],
            ]
    endpoint = api_prefix + '/move'
    app.post(
        endpoint,
        data=json.dumps({'user': user.address, 'direction': 1}),  # Up
        content_type='application/json'
    )
    with app as c:
        with c.session_transaction() as sess:
            assert not sess['has_paid']
            assert sess['state']['gameover']
