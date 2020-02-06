import json
from webserver import exceptions
from webserver import schemas
from webserver.signing import (
    prepare_structured_nonce_for_signing,
)
from webserver.config import (
    ARCADE_ADDRESS,
)
from web3 import (
    Account,
)


def test_confirm_payment_success(mocker, app, api_prefix, user):
    nonce = b'\x01' * 32
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = nonce
    structured_msg = prepare_structured_nonce_for_signing(
        ARCADE_ADDRESS,
        nonce,
    )
    signature = Account.sign_message(structured_msg, user.key)
    contract = mocker.patch('webserver.endpoints.payment.contract')
    contract.functions.getNonce.return_value.call.return_value = nonce  # noqa: E501
    mocker.patch('webserver.endpoints.payment.wait_for_transaction_receipt')  # noqa: E501
    response = app.get(
        api_prefix + '/payment-confirmation',
        query_string={
            'signature': signature['signature'].hex(),
            'txhash': '0x',
        },
    )
    output = json.loads(response.data)
    errors = schemas.SignedGamestate().validate(output)
    assert not errors
    with app as c:
        with c.session_transaction() as sess:
            assert sess['paid']


def test_recovered_address_is_user(mocker, app, api_prefix, user):
    nonce = b'\x01' * 32
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = nonce
    structured_msg = prepare_structured_nonce_for_signing(
        ARCADE_ADDRESS,
        nonce,
    )
    signature = Account.sign_message(structured_msg, user.key)
    contract = mocker.patch('webserver.endpoints.payment.contract')
    contract.functions.getNonce.return_value.call.return_value = nonce  # noqa: E501
    mocker.patch('webserver.endpoints.payment.wait_for_transaction_receipt')  # noqa: E501
    app.get(
        api_prefix + '/payment-confirmation',
        query_string={
            'signature': signature['signature'].hex(),
            'txhash': '0x',
        },
    )
    with app as c:
        with c.session_transaction() as sess:
            assert sess['recoveredAddress'] == user.address


def test_already_paid(app, api_prefix, user):
    """
    It should fail with exception UnexpectedPaymentAttempt when trying to pay
    without first generating a new random nonce value
    """
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = True
    response = app.get(
        api_prefix + '/payment-confirmation',
    )
    output = json.loads(response.data)
    assert output['message'] == exceptions.UnexpectedPaymentAttempt.message


def test_empty_nonce(app, api_prefix, user):
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
    nonce = b'\x01' * 32
    incorrect_nonce = b'\x02' * 32
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = nonce
            sess['address'] = user.address
    structured_msg = prepare_structured_nonce_for_signing(
        ARCADE_ADDRESS,
        nonce,
    )
    signature = Account.sign_message(structured_msg, user.key)
    contract = mocker.patch('webserver.endpoints.payment.contract')
    contract.functions.getNonce.return_value.call.return_value = incorrect_nonce  # noqa: E501
    mocker.patch('webserver.endpoints.payment.wait_for_transaction_receipt')  # noqa: E501
    response = app.get(
        api_prefix + '/payment-confirmation',
        query_string={
            'signature': signature['signature'].hex(),
            'txhash': '0x',
        },
    )
    output = json.loads(response.data)
    assert output['message'] == exceptions.UnexpectedContractNonce.message
