from webserver.arcade import (
    Arcade,
)
from webserver.signing import (
    sign_score,
)
import random
from webserver.exceptions import (
    PaymentError,
)


def test_new_gamecode(mocker):
    random_value = '0x1234'
    mocker.patch('webserver.arcade.random_32bytes').return_value = random_value
    expected_gamecode = random_value
    gamecode = Arcade.new_gamecode()
    assert gamecode == expected_gamecode


def test_new_session_id(mocker):
    random_value = '0x1234'
    mocker.patch('webserver.arcade.random_32bytes').return_value = random_value
    expected_session_id = random_value
    session_id = Arcade.new_session_id()
    assert session_id == expected_session_id


def test_confirm_payment_success(user, owner, monkeypatch, mocker):
    gamecode = '0x1234'

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = gamecode

    error = Arcade.confirm_payment(
        user.address,
        gamecode,
    )
    assert error is None


def test_confirm_payment_user_hasnt_uploaded_gamecode(user, owner, mocker):
    random_value = '0x1234'
    gamecode = random_value
    old_gamecode = '0x2345'

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = old_gamecode

    error = Arcade.confirm_payment(
        user.address,
        gamecode,
    )
    assert error == PaymentError


def test_new_game(user, owner, monkeypatch):
    random.seed(1234)
    monkeypatch.setattr("webserver.signing.PRIV", owner.key)
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
    next_state, signature = arcade.new_game()
    assert next_state == expected_state
    assert signature == expected_signature


def test_update_game(user, owner, monkeypatch):
    random.seed(1234)
    monkeypatch.setattr("webserver.signing.PRIV", owner.key)
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
    next_state, signature = arcade.update_game(current_state, update)
    assert next_state == expected_state
    assert signature == expected_signature
