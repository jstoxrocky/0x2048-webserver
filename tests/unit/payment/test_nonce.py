import json
from webserver import exceptions


def test_nonce_success(mocker, app, api_prefix, user):
    """
    It should succeed
    """
    nonce = 123456
    generate_random_nonce = mocker.patch('webserver.endpoints.payment.state_channel.generate_random_nonce')  # noqa: E501
    generate_random_nonce.return_value = nonce
    response = app.get(
        api_prefix + '/nonce',
    )
    output = json.loads(response.data)
    assert output == {'nonce': nonce}

    with app as c:
        with c.session_transaction() as sess:
            assert sess['nonce'] == nonce


def test_nonce_already_paid(app, api_prefix, user):
    """
    It should fail with exception UnexpectedPaymentAttempt
    """
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = True
    response = app.get(
        api_prefix + '/nonce',
    )
    output = json.loads(response.data)
    assert output['message'] == exceptions.UnexpectedPaymentAttempt.message


def test_nonce_already_generated(app, api_prefix, user):
    """
    It should fail with exception UnexpectedNonceGenerationAttempt
    """
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = 987654
    response = app.get(
        api_prefix + '/nonce',
    )
    output = json.loads(response.data)
    assert output['message'] == exceptions.UnexpectedNonceGenerationAttempt.message  # noqa: E501
