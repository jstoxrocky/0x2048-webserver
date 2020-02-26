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
    prepare_structured_nonce_for_signing,
)
from webserver.exceptions import (
    ChallengeResponseValidationError,
    UnpaidSessionValidationError,
    PaymentError,
)
from hexbytes import (
    HexBytes,
)


def test_happy_path(user, mocker):
    # Challenge Response
    arcade_response = Arcade.new_session()
    signable_message = prepare_structured_nonce_for_signing(
        arcade_response['challenge']
    )
    signature = Account.sign_message(signable_message, user.key)
    challenge_response = {
        'session_id': arcade_response['session_id'],
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'challenge': arcade_response['challenge']
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(arcade_response['session_id'], json.dumps(unpaid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value \
        .call.return_value = arcade_response['challenge']

    # Run
    event, context = challenge_response, None
    signed_gamestate = json.loads(new_game(event, context))
    session = json.loads(redis.get(arcade_response['session_id']))

    # Test
    errors = SignedGamestate().validate(signed_gamestate)
    assert not errors
    errors = PaidSession().validate(session)
    assert not errors


def test_user_provides_bad_challenge_response(user, mocker):
    # Challenge Response
    challenge_response = {}

    # Run / Test
    event, context = challenge_response, None
    with pytest.raises(ChallengeResponseValidationError):
        new_game(event, context)


def test_user_has_no_session_id_in_redis(user, mocker):
    # Challenge Response
    arcade_response = Arcade.new_session()
    signable_message = prepare_structured_nonce_for_signing(
        arcade_response['challenge']
    )
    signature = Account.sign_message(signable_message, user.key)
    challenge_response = {
        'session_id': arcade_response['session_id'],
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
    event, context = challenge_response, None
    with pytest.raises(UnpaidSessionValidationError):
        new_game(event, context)


def test_user_has_incorrect_session(user, mocker):
    # Challenge Response
    arcade_response = Arcade.new_session()
    signable_message = prepare_structured_nonce_for_signing(
        arcade_response['challenge']
    )
    signature = Account.sign_message(signable_message, user.key)
    challenge_response = {
        'session_id': arcade_response['session_id'],
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
    redis.set(arcade_response['session_id'], json.dumps(unpaid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Run / Test
    event, context = challenge_response, None
    with pytest.raises(UnpaidSessionValidationError):
        new_game(event, context)


def test_payment_doesnt_confirm(user, mocker):
    # Challenge Response
    arcade_response = Arcade.new_session()
    signable_message = prepare_structured_nonce_for_signing(
        arcade_response['challenge']
    )
    signature = Account.sign_message(signable_message, user.key)
    challenge_response = {
        'session_id': arcade_response['session_id'],
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'challenge': arcade_response['challenge']
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(arcade_response['session_id'], json.dumps(unpaid_session))
    mocker.patch('webserver.new_game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = '0x0'

    # Run
    event, context = challenge_response, None
    with pytest.raises(PaymentError):
        new_game(event, context)
