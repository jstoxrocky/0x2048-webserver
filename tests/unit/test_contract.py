from webserver.contract import (
    confirm_payment,
)


def test_confirm_payment(mocker):
    random_value = '0x1234'
    gamecode = random_value

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = random_value
    signer = '0xdeadbeefbadfooddead'
    output = confirm_payment(signer, gamecode)
    assert output is True
