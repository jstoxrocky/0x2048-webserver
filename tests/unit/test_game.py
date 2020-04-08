import fakeredis
import json
import pytest
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
from webserver.exceptions import (
    AddressPayloadValidationError,
    UnpaidSessionValidationError,
    PaymentError,
)


def test_happy_path(user, mocker):
    gamecode = Arcade.new_gamecode()
    session_id = Arcade.new_session_id()
    address_payload = {
        'session_id': session_id,
        'address': user.address,
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
    signed_gamestate = json.loads(get_game(address_payload))
    session = json.loads(redis.get(session_id))

    # Test
    errors = SignedGamestate().validate(signed_gamestate)
    assert not errors
    errors = PaidSession().validate(session)
    assert not errors


def test_user_grabs_someone_elses_gamecode(user, mocker):
    honest_user = user

    gamecode_for_liar_user = Arcade.new_gamecode()
    session_id = Arcade.new_session_id()
    # Liar pretends to be honest
    address_payload = {
        'session_id': session_id,
        'address': honest_user.address,
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'gamecode': gamecode_for_liar_user,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Contract
    gamecode_for_honest_user = Arcade.new_gamecode()
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getNonce.return_value \
        .call.return_value = gamecode_for_honest_user

    # Run / Test
    with pytest.raises(PaymentError):
        get_game(address_payload)


def test_user_provides_bad_address_payload(user, mocker):
    address_payload = {}

    # Run / Test
    with pytest.raises(AddressPayloadValidationError):
        get_game(address_payload)


def test_user_has_no_session_id_in_redis(user, mocker):
    session_id = Arcade.new_session_id()
    address_payload = {
        'session_id': session_id,
        'address': user.address,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(UnpaidSessionValidationError):
        get_game(address_payload)


def test_user_has_incorrect_session(user, mocker):
    session_id = Arcade.new_session_id()
    address_payload = {
        'session_id': session_id,
        'address': user.address,
    }

    # UnpaidSession
    unpaid_session = {}
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(UnpaidSessionValidationError):
        get_game(address_payload)


def test_payment_doesnt_confirm(user, mocker):
    gamecode = Arcade.new_gamecode()
    session_id = Arcade.new_session_id()
    address_payload = {
        'session_id': session_id,
        'address': user.address,
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
        get_game(address_payload)
