import json
from webserver import exceptions
from webserver import schemas
from eth_utils import (
    decode_hex,
)
from webserver import state_channel


def test_confirm_payment_success(mocker, app, api_prefix, user):
    nonce = '0x01'
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = nonce
            sess['address'] = user.address

    signature = state_channel.raw_sign(
        state_channel.prepare_messageHash_for_signing(nonce),
        user.privateKey,
    )
    contract = mocker.patch('webserver.endpoints.payment.contract')
    contract.functions.getNonce.return_value.call.return_value = decode_hex(nonce)  # noqa: E501
    mocker.patch('webserver.endpoints.payment.wait_for_transaction_receipt')  # noqa: E501
    response = app.get(
        api_prefix + '/payment-confirmation',
        query_string={
            'signature': signature.to_hex(),
            'txhash': '0x',
        },
    )
    output = json.loads(response.data)
    errors = schemas.SignedGamestate().validate(output)
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
    nonce = '0x01'
    incorrect_nonce = '0x02'
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False
            sess['nonce'] = nonce
            sess['address'] = user.address
    signature = state_channel.raw_sign(
        state_channel.prepare_messageHash_for_signing(nonce),
        user.privateKey,
    )
    contract = mocker.patch('webserver.endpoints.payment.contract')
    contract.functions.getNonce.return_value.call.return_value = incorrect_nonce  # noqa: E501
    mocker.patch('webserver.endpoints.payment.wait_for_transaction_receipt')  # noqa: E501
    response = app.get(
        api_prefix + '/payment-confirmation',
        query_string={
            'signature': signature.to_hex(),
            'txhash': '0x',
        },
    )
    output = json.loads(response.data)
    assert output['message'] == exceptions.UnexpectedContractNonce.message
