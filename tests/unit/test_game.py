import fakeredis
import json
import pytest
from web3 import (
    Account,
)
from webserver.game import (
    game as get_game,
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
    SignaturePayloadValidationError,
    UnpaidSessionValidationError,
    PaymentError,
)
from hexbytes import (
    HexBytes,
)


def test_happy_path(user, mocker):
    # Gamecode Response
    gamecode = Arcade.new_gamecode()
    session_id = Arcade.new_session_id()
    signable_message = prepare_structured_gamecode_for_signing(
        gamecode,
    )
    signature = Account.sign_message(signable_message, user.key)
    signature_payload = {
        'session_id': session_id,
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'gamecode': gamecode,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value \
        .call.return_value = gamecode

    # Run
    signed_gamestate = json.loads(get_game(signature_payload))
    session = json.loads(redis.get(session_id))

    # Test
    errors = SignedGamestate().validate(signed_gamestate)
    assert not errors
    errors = PaidSession().validate(session)
    assert not errors


def test_user_provides_bad_signature_payload(user, mocker):
    # Signature Payload
    signature_payload = {}

    # Run / Test
    with pytest.raises(SignaturePayloadValidationError):
        get_game(signature_payload)


def test_user_has_no_session_id_in_redis(user, mocker):
    # Gamecode Response
    gamecode = Arcade.new_gamecode()
    session_id = Arcade.new_session_id()
    signable_message = prepare_structured_gamecode_for_signing(
        gamecode,
    )
    signature = Account.sign_message(signable_message, user.key)
    signature_payload = {
        'session_id': session_id,
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(UnpaidSessionValidationError):
        get_game(signature_payload)


def test_user_has_incorrect_session(user, mocker):
    # Gamecode Response
    gamecode = Arcade.new_gamecode()
    session_id = Arcade.new_session_id()
    signable_message = prepare_structured_gamecode_for_signing(
        gamecode,
    )
    signature = Account.sign_message(signable_message, user.key)
    signature_payload = {
        'session_id': session_id,
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
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(UnpaidSessionValidationError):
        get_game(signature_payload)


def test_payment_doesnt_confirm(user, mocker):
    # Gamecode Response
    gamecode = Arcade.new_gamecode()
    session_id = Arcade.new_session_id()
    signable_message = prepare_structured_gamecode_for_signing(
        gamecode,
    )
    signature = Account.sign_message(signable_message, user.key)
    signature_payload = {
        'session_id': session_id,
        'signature': {
            'v': signature['v'],
            'r': HexBytes(signature['r']).hex(),
            's': HexBytes(signature['s']).hex(),
        }
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'gamecode': gamecode,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value.call.return_value = '0x0'

    # Run
    with pytest.raises(PaymentError):
        get_game(signature_payload)
