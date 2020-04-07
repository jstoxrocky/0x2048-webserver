from webserver.arcade import (
    Arcade,
)
from webserver.signing import (
    sign_score,
    prepare_structured_gamecode_for_signing,
)
from web3 import (
    Account,
)
import random


def test_gamecode(mocker):
    gamecode = '0x1234'
    mocker.patch('webserver.arcade.generate_gamecode').return_value = gamecode
    expected_gamecode = gamecode
    gamecode = Arcade.new_gamecode()
    assert gamecode == expected_gamecode


def test_recover_signer(user):
    random.seed(1234)
    gamecode = '0x1234'

    message = prepare_structured_gamecode_for_signing(gamecode)
    signature = Account.sign_message(message, user.key)
    address = Arcade.recover_signer(
        gamecode,
        signature['v'],
        signature['r'],
        signature['s'],
    )
    assert address == user.address


def test_confirm_payment_success(user, owner, monkeypatch, mocker):
    random.seed(1234)
    gamecode = '0x1234'

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = gamecode

    message = prepare_structured_gamecode_for_signing(gamecode)
    signature = Account.sign_message(message, user.key)
    address = Arcade.recover_signer(
        gamecode,
        signature['v'],
        signature['r'],
        signature['s'],
    )
    success = Arcade.confirm_payment(
        address,
        gamecode,
    )
    assert success


def test_confirm_payment_user_hasnt_uploaded_gamecode(user2, owner, mocker):
    random.seed(1234)
    gamecode = '0x1234'
    old_gamecode = '0x2345'

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = old_gamecode

    message = prepare_structured_gamecode_for_signing(gamecode)
    signature = Account.sign_message(message, user2.key)
    address = Arcade.recover_signer(
        gamecode,
        signature['v'],
        signature['r'],
        signature['s'],
    )
    success = Arcade.confirm_payment(
        address,
        gamecode,
    )
    assert not success


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
    new_game = Arcade.new_game(user.address)
    assert new_game == expected_signed_game_state


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

    updated_game = Arcade.update_game(
        user.address,
        current_state=current_state,
        update=direction,
    )
    assert updated_game == expected_signed_game_state
