import json
from webserver import exceptions
from webserver import state_channel


def test_confirm_address_success(mocker, app, api_prefix, user):
    nonce = 987654
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = nonce
    prepare_message_for_signing = mocker.patch('webserver.endpoints.payment.state_channel.prepare_messageHash_for_signing')  # noqa: E501
    prepare_message_for_signing.return_value = b''
    recover = mocker.patch('webserver.endpoints.payment.state_channel.recover')  # noqa: E501
    recover.return_value = user.address

    expected = {'success': True}
    response = app.get(
        api_prefix + '/address-confirmation',
        query_string={'signature': '0x'},
    )
    output = json.loads(response.data)
    assert output == expected

    with app as c:
        with c.session_transaction() as sess:
            assert sess['address'] == user.address


def test_integrated_confirm_address_success(mocker, app, api_prefix, user):
    nonce = b'Joey to the World!'
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = nonce
    signature = state_channel.raw_sign(
        state_channel.prepare_messageHash_for_signing(nonce),
        user.privateKey,
    )
    recover = mocker.patch('webserver.endpoints.payment.request')  # noqa: E501
    recover.get_json.return_value = signature.to_bytes()
    expected = {'success': True}
    response = app.get(
        api_prefix + '/address-confirmation',
        query_string={'signature': '0x'},
    )
    output = json.loads(response.data)
    assert output == expected

    with app as c:
        with c.session_transaction() as sess:
            assert sess['address'] == user.address


def test_confirm_address_already_paid(app, api_prefix, user):
    """
    It should fail with exception UnexpectedPaymentAttempt
    """
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = True
    response = app.get(
        api_prefix + '/address-confirmation',
    )
    output = json.loads(response.data)
    assert output['message'] == exceptions.UnexpectedPaymentAttempt.message


def test_confirm_address_empty_nonce(app, api_prefix, user):
    """
    It should fail with exception UnexpectedPaymentAttempt
    """
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = None
    response = app.get(
        api_prefix + '/address-confirmation',
    )
    output = json.loads(response.data)
    assert output['message'] == exceptions.UnexpectedEmptyNonce.message
