import fakeredis
import json
import pytest
from webserver.game import (
    game as get_game,
)
from webserver.schemas import (
    SignedGamestateResponse,
    PaidSession,
)
from webserver.arcade import (
    Arcade,
)
from webserver.exceptions import (
    PaymentLocatorPayloadValidationError,
    UnpaidSessionValidationError,
    PaymentError,
)
from webserver.game_config import (
    TWENTY_FORTY_EIGHT,
)


def test_happy_path(user, mocker):
    payment_code = Arcade.new_payment_code()
    session_id = Arcade.new_session_id()
    game_id = TWENTY_FORTY_EIGHT
    payment_locator_payload = {
        'session_id': session_id,
        'address': user.address,
        'game_id': game_id,
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'payment_code': payment_code,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getPaymentCode.return_value \
        .call.return_value = payment_code

    # Run
    signed_gamestate = json.loads(get_game(payment_locator_payload))
    session = json.loads(redis.get(session_id))

    # Test
    errors = SignedGamestateResponse().validate(signed_gamestate)
    assert not errors
    errors = PaidSession().validate(session)
    assert not errors


def test_user_grabs_someone_elses_payment_code(user, mocker):
    honest_user = user

    payment_code_for_liar_user = Arcade.new_payment_code()
    session_id = Arcade.new_session_id()
    game_id = TWENTY_FORTY_EIGHT

    # Liar pretends to be honest
    payment_locator_payload = {
        'session_id': session_id,
        'address': honest_user.address,
        'game_id': game_id,
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'payment_code': payment_code_for_liar_user,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Contract
    payment_code_for_honest_user = Arcade.new_payment_code()
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getPaymentCode.return_value \
        .call.return_value = payment_code_for_honest_user

    # Run / Test
    with pytest.raises(PaymentError):
        get_game(payment_locator_payload)


def test_user_provides_bad_address_payload(user, mocker):
    payment_locator_payload = {}

    # Run / Test
    with pytest.raises(PaymentLocatorPayloadValidationError):
        get_game(payment_locator_payload)


def test_user_has_no_session_id_in_redis(user, mocker):
    session_id = Arcade.new_session_id()
    game_id = TWENTY_FORTY_EIGHT
    payment_locator_payload = {
        'session_id': session_id,
        'address': user.address,
        'game_id': game_id,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(UnpaidSessionValidationError):
        get_game(payment_locator_payload)


def test_user_has_incorrect_session(user, mocker):
    session_id = Arcade.new_session_id()
    game_id = TWENTY_FORTY_EIGHT
    payment_locator_payload = {
        'session_id': session_id,
        'address': user.address,
        'game_id': game_id,
    }

    # UnpaidSession
    unpaid_session = {}
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Run / Test
    with pytest.raises(UnpaidSessionValidationError):
        get_game(payment_locator_payload)


def test_payment_doesnt_confirm(user, mocker):
    payment_code = Arcade.new_payment_code()
    session_id = Arcade.new_session_id()
    game_id = TWENTY_FORTY_EIGHT
    payment_locator_payload = {
        'session_id': session_id,
        'address': user.address,
        'game_id': game_id,
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'payment_code': payment_code,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch('webserver.game.redis.Redis').return_value = redis

    # Contract
    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getPaymentCode.return_value.call.return_value = '0x0'

    # Run
    with pytest.raises(PaymentError):
        get_game(payment_locator_payload)


def test_game_id_is_not_real(user, mocker):
    session_id = Arcade.new_session_id()
    game_id = '0x34a8bcaf7e336f18e5f5eeca59336015b6cdfa5c66f1364a19b7c539971cfbcf'  # noqa: E501
    payment_locator_payload = {
        'session_id': session_id,
        'address': user.address,
        'game_id': game_id,
    }

    # Run / Test
    with pytest.raises(PaymentLocatorPayloadValidationError):
        get_game(payment_locator_payload)
