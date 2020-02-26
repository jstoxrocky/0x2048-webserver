from webserver.contract import (
    confirm_payment,
)


def test_confirm_payment(mocker):
    nonce = '0x1234'
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = nonce
    signer = '0xdeadbeefbadfooddead'
    challenge = nonce
    output = confirm_payment(signer, challenge)
    assert output is True
