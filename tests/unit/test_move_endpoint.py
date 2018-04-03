import json
from webserver import exceptions
from webserver.gameplay import (
    new,
)
from webserver import schemas
from webserver.config import (
    INITIAL_STATE,
)


def test_user_has_not_paid(mocker, app, api_prefix):
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
    endpoint = api_prefix + '/move'
    response = app.post(
        endpoint,
        data=json.dumps({}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    assert response.status_code == exceptions.UnexpectedMoveAttemptWithoutPaying.status_code  # noqa: E501
    assert output['message'] == exceptions.UnexpectedMoveAttemptWithoutPaying.message  # noqa: E501


def test_validation_error(mocker, app, api_prefix):
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = True
    validate = mocker.patch('webserver.endpoints.move.schemas.Move.validate')
    validate.return_value = {'error_key': ['error_message']}
    endpoint = api_prefix + '/move'
    response = app.post(
        endpoint,
        data=json.dumps({}),
        content_type='application/json'
    )
    output = json.loads(response.data)
    assert response.status_code == exceptions.ValidationError.status_code
    assert output['message'] == exceptions.ValidationError.message


def test_output_validates(mocker, app, api_prefix, user):
    with app as c:
        with c.session_transaction() as sess:
            sess['recoveredAddress'] = user.address
            sess['paid'] = True
    validate = mocker.patch('webserver.endpoints.move.schemas.Move.validate')
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
    errors = schemas.SignedGamestate().validate(output)
    assert not errors
    with app as c:
        with c.session_transaction() as sess:
            assert not sess['state']['gameover']


def test_gameover(mocker, app, api_prefix, user):
    with app as c:
        with c.session_transaction() as sess:
            sess['recoveredAddress'] = user.address
            sess['paid'] = True
    validate = mocker.patch('webserver.endpoints.move.schemas.Move.validate')
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
            assert sess['state']['gameover']
