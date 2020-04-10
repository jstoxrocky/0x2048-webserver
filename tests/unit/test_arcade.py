from webserver.arcade import (
    Arcade,
)
from webserver.signing import (
    sign_score,
)
import random
from eth_utils import (
    keccak,
)
from hexbytes import (
    HexBytes,
)
from webserver.game_config import (
    TWENTY_FORTY_EIGHT,
)


def test_game_info(mocker):
    game_id = TWENTY_FORTY_EIGHT
    highscore = 1000
    jackpot = 100
    expected_game_info = {
        'id': game_id,
        'name': '2048',
        'highscore': highscore,
        'jackpot': jackpot,
    }

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getHighscore \
        .return_value.call.return_value = highscore
    contract.functions.getJackpot \
        .return_value.call.return_value = jackpot

    game_info = Arcade.game_info(game_id)
    assert game_info == expected_game_info


def test_new_payment_code(mocker):
    random_value = '0x1234'
    mocker.patch('webserver.arcade.random_32bytes').return_value = random_value
    expected_payment_code = random_value
    payment_code = Arcade.new_payment_code()
    assert payment_code == expected_payment_code


def test_new_session_id(mocker):
    random_value = '0x1234'
    mocker.patch('webserver.arcade.random_32bytes').return_value = random_value
    expected_session_id = random_value
    session_id = Arcade.new_session_id()
    assert session_id == expected_session_id


def test_confirm_payment_success(user, owner, monkeypatch, mocker):
    payment_code = HexBytes(keccak(text='ABC')).hex()
    game_id = HexBytes(keccak(text='123')).hex()

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getPaymentCode \
        .return_value.call.return_value = payment_code

    error = Arcade.confirm_payment(
        game_id,
        user.address,
        payment_code,
    )
    assert error is False


def test_confirm_payment_user_hasnt_uploaded_payment_code(user, owner, mocker):
    old_payment_code = HexBytes(keccak(text='XYZ')).hex()
    payment_code = HexBytes(keccak(text='ABC')).hex()
    game_id = HexBytes(keccak(text='123')).hex()

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getPaymentCode.return_value.call.return_value = (
        old_payment_code
    )

    error = Arcade.confirm_payment(
        game_id,
        user.address,
        payment_code,
    )
    assert error is True


def test_new_game(user, owner, monkeypatch):
    random.seed(1234)
    monkeypatch.setattr("webserver.signing.PRIV", owner.key)
    game_id = TWENTY_FORTY_EIGHT
    expected_state = {
        'board': [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, 0]],
        'score': 0,
        'gameover': False,
    }
    score = 0
    signed_score = sign_score(user.address, score)
    expected_signature = {
        'v': signed_score['v'],
        'r': signed_score['r'],
        's': signed_score['s'],
    }
    arcade = Arcade(player=user.address)
    next_state, signature = arcade.new_game(game_id)
    assert next_state == expected_state
    assert signature == expected_signature


def test_update_game(user, owner, monkeypatch):
    random.seed(1234)
    monkeypatch.setattr("webserver.signing.PRIV", owner.key)
    game_id = TWENTY_FORTY_EIGHT
    current_state = {
        'board': [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, 0]],
        'score': 0,
        'gameover': False,
    }
    update = 2

    expected_state = {
        'board': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 4, 2, 0]],
        'score': 0,
        'gameover': False,
    }
    score = 0
    signed_score = sign_score(user.address, score)
    expected_signature = {
        'v': signed_score['v'],
        'r': signed_score['r'],
        's': signed_score['s'],
    }
    arcade = Arcade(player=user.address)
    next_state, signature = arcade.update_game(game_id, current_state, update)
    assert next_state == expected_state
    assert signature == expected_signature
