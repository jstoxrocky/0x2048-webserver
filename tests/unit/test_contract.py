from webserver.contract import (
    confirm_payment,
)
from eth_utils import (
    keccak,
)
from hexbytes import (
    HexBytes,
)


def test_confirm_payment(mocker):
    payment_code = HexBytes(keccak(text='ABC')).hex()
    game_id = HexBytes(keccak(text='123')).hex()

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getPaymentCode \
        .return_value.call.return_value = payment_code

    signer = '0xdeadbeefbadfooddead'
    error = confirm_payment(game_id, signer, payment_code)
    assert error is False
