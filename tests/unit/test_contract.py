from webserver.contract import (
    confirm_payment,
)


def test_confirm_payment(mocker):
    gamecode = '0x1234'
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = gamecode
    signer = '0xdeadbeefbadfooddead'
    output = confirm_payment(signer, gamecode)
    assert output is True
