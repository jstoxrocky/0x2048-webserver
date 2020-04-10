from webserver.contract import (
    confirm_payment,
    get_game_stats,
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


def test_get_game_stats(mocker):
    game_id = HexBytes(keccak(text='123')).hex()
    highscore = 10
    jackpot = 9

    expected_game_stats = {
        'highscore': highscore,
        'jackpot': jackpot,
    }

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getHighscore.return_value.call.return_value = highscore
    contract.functions.getJackpot.return_value.call.return_value = jackpot

    game_stats = get_game_stats(game_id)
    assert game_stats == expected_game_stats
