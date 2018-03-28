import json
from webserver import exceptions
from webserver import schemas


def test_confirm_payment_success(mocker, app, api_prefix, user):
    nonce = 987654
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = nonce
            sess['address'] = user.address
    contract = mocker.patch('webserver.endpoints.payment.contract')
    contract.functions.getNonce.return_value.call.return_value = nonce  # noqa: E501
    response = app.get(
        api_prefix + '/payment-confirmation',
        query_string={'signature': '0x'},
    )
    output = json.loads(response.data)
    errors = schemas.SignedGamestateSchema().validate(output)
    assert not errors
    with app as c:
        with c.session_transaction() as sess:
            assert sess['paid']


def test_confirm_address_already_paid(app, api_prefix, user):
    """
    It should fail with exception UnexpectedPaymentAttempt
    """
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = True
    response = app.get(
        api_prefix + '/payment-confirmation',
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
        api_prefix + '/payment-confirmation',
    )
    output = json.loads(response.data)
    assert output['message'] == exceptions.UnexpectedEmptyNonce.message


def test_incorrect_contract_nonce(mocker, app, api_prefix, user):
    nonce = 987654
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = nonce
    contract = mocker.patch('webserver.endpoints.payment.contract')
    contract.functions.getNonce.return_value.call.return_value = nonce + 1  # noqa: E501
    response = app.get(
        api_prefix + '/payment-confirmation',
        query_string={'signature': '0x'},
    )
    output = json.loads(response.data)
    assert output['message'] == exceptions.UnexpectedContractNonce.message
