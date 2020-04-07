import fakeredis
import json
import pytest
from web3 import (
    Account,
)
from webserver.new_game import (
    new_game,
)
from webserver.schemas import (
    SignedGamestate,
    PaidSession,
)
from webserver.arcade import (
    Arcade,
)
from webserver.signing import (
    prepare_structured_gamecode_for_signing,
)
from webserver.exceptions import (
    AuthenticationResponseValidationError,
    UnpaidSessionValidationError,
    PaymentError,
)
from hexbytes import (
    HexBytes,
)


def test_happy_path(user, mocker):
    gamecode = Arcade.new_gamecode()
    signable_message = prepare_structured_gamecode_for_signing(
        gamecode,
    )
    signature = Account.sign_message(signable_message, user.key)
    auth_response = {
        'gamecode': gamecode,
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(gamecode, json.dumps(unpaid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value \
        .call.return_value = gamecode

    # Run
    signed_gamestate = json.loads(new_game(auth_response))
    session = json.loads(redis.get(gamecode))

    # Test
    errors = SignedGamestate().validate(signed_gamestate)
    assert not errors
    errors = PaidSession().validate(session)
    assert not errors


def test_user_provides_bad_auth_response(user, mocker):
    auth_response = {}

    # Run / Test
    with pytest.raises(AuthenticationResponseValidationError):
        new_game(auth_response)


def test_user_has_no_gamecode_in_redis(user, mocker):
    gamecode = Arcade.new_gamecode()
    signable_message = prepare_structured_gamecode_for_signing(
        gamecode
    )
    signature = Account.sign_message(signable_message, user.key)
    auth_response = {
        'gamecode': gamecode,
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(UnpaidSessionValidationError):
        new_game(auth_response)


def test_user_has_incorrect_session(user, mocker):
    gamecode = Arcade.new_gamecode()
    signable_message = prepare_structured_gamecode_for_signing(
        gamecode
    )
    signature = Account.sign_message(signable_message, user.key)
    auth_response = {
        'gamecode': gamecode,
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }

    # UnpaidSession
    unpaid_session = {}
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(gamecode, json.dumps(unpaid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(UnpaidSessionValidationError):
        new_game(auth_response)


def test_payment_doesnt_confirm(user, mocker):
    gamecode = Arcade.new_gamecode()
    signable_message = prepare_structured_gamecode_for_signing(
        gamecode
    )
    signature = Account.sign_message(signable_message, user.key)
    auth_response = {
        'gamecode': gamecode,
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(gamecode, json.dumps(unpaid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = '0x0'

    # Run
    with pytest.raises(PaymentError):
        new_game(auth_response)
