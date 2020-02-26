from webserver.arcade import (
    Arcade,
)
from webserver.signing import (
    sign_score,
    prepare_structured_nonce_for_signing,
)
from web3 import (
    Account,
)
import random


def test_new_session(mocker):
    nonce = '0x1234'
    mocker.patch('webserver.arcade.nonce').return_value = nonce
    expected_arcade_response = {
        'session_id': nonce,
        'challenge': nonce,
    }
    arcade_response = Arcade.new_session()
    assert arcade_response == expected_arcade_response


def test_confirm_payment_success(user, owner, monkeypatch, mocker):
    random.seed(1234)
    nonce = '0x1234'

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = nonce

    message = prepare_structured_nonce_for_signing(nonce)
    signature = Account.sign_message(message, user.key)
    payment_confirmation = Arcade.confirm_payment(
        nonce,
        signature['v'],
        signature['r'],
        signature['s'],
    )
    assert payment_confirmation['recovered_address'] == user.address
    assert payment_confirmation['success']


def test_confirm_payment_user_hasnt_uploaded_challenge(user2, owner, mocker):
    random.seed(1234)
    nonce = '0x1234'
    old_nonce = '0x2345'

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = old_nonce

    message = prepare_structured_nonce_for_signing(nonce)
    signature = Account.sign_message(message, user2.key)
    payment_confirmation = Arcade.confirm_payment(
        nonce,
        signature['v'],
        signature['r'],
        signature['s'],
    )
    assert not payment_confirmation['success']


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
    expected_signed_game_state = {
        'state': expected_state,
        'signed_score': {
            'v': signed_score['v'],
            'r': signed_score['r'],
            's': signed_score['s'],
        },
    }
    arcade = Arcade(player_address=user.address)
    signed_game_state = arcade.new_game()
    assert signed_game_state == expected_signed_game_state


def test_update_game(user, owner, monkeypatch):
    random.seed(1234)
    monkeypatch.setattr("webserver.signing.PRIV", owner.key)
    current_state = {
        'board': [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, 0]],
        'score': 0,
        'gameover': False,
    }
    direction = 2

    expected_state = {
        'board': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 4, 2, 0]],
        'score': 0,
        'gameover': False,
    }
    score = 0
    signed_score = sign_score(user.address, score)
    expected_signed_game_state = {
        'state': expected_state,
        'signed_score': {
            'v': signed_score['v'],
            'r': signed_score['r'],
            's': signed_score['s'],
        },
    }

    arcade = Arcade(player_address=user.address)
    signed_game_state = arcade.update_game(current_state, update=direction)
    assert signed_game_state == expected_signed_game_state
