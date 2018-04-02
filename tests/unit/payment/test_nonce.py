import json
from webserver import schemas


def test_nonce_success(mocker, app, api_prefix, user):
    """
    It should succeed and overwrite session.nonce and session.paid
    """
    nonce = '0x987654'
    with app as c:
        with c.session_transaction() as sess:
            sess['nonce'] = nonce
            sess['paid'] = True
    generate_random_nonce = mocker.patch('webserver.endpoints.payment.state_channel.generate_random_nonce')  # noqa: E501
    generate_random_nonce.return_value = nonce
    response = app.get(
        api_prefix + '/nonce',
    )
    output = json.loads(response.data)
    errors = schemas.Nonce().validate(output)
    assert not errors
    with app as c:
        with c.session_transaction() as sess:
            assert sess['nonce'] == nonce
            assert not sess['paid']
