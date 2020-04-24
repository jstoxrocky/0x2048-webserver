import fakeredis
import json
import pytest
from arcade_protocol import (
    GameInterface,
)
from webserver.payment_confirmation import (
    payment_confirmation as get_payment_confirmation,
)
from webserver.schemas import (
    SignedGamestateResponse,
    PaidSession,
)
from webserver.exceptions import (
    PaymentLocatorPayloadValidationError,
    UnpaidSessionValidationError,
    PaymentError,
)
from webserver.session import (
    new_session,
)


ADDRESS = '0x0A34371d4BB7c49Ec9e4c156b525eA7417f63e7A'


def test_happy_path(user, mocker, monkeypatch):
    payment_code = GameInterface.new_payment_code()
    session_id = new_session()
    payment_locator_payload = {
        'session_id': session_id,
        'user': user.address,
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'payment_code': payment_code,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch(
        'webserver.payment_confirmation.redis.Redis',
    ).return_value = redis

    # Contract
    monkeypatch.setattr("webserver.payment_confirmation.ADDRESS", ADDRESS)
    contract = mocker.patch(
        'webserver.payment_confirmation.arcade_protocol.Contract',
    ).return_value
    contract.get_payment_code.return_value = payment_code
    contract.address = ADDRESS

    # Run
    signed_gamestate = json.loads(
        get_payment_confirmation(payment_locator_payload),
    )
    session = json.loads(redis.get(session_id))

    # Test
    errors = SignedGamestateResponse().validate(signed_gamestate)
    assert not errors
    errors = PaidSession().validate(session)
    assert not errors


def test_user_grabs_someone_elses_payment_code(user, mocker):
    honest_user = user

    actual_payment_code_the_user_got = GameInterface.new_payment_code()
    session_id = new_session()

    # Liar pretends to be honest
    payment_locator_payload = {
        'session_id': session_id,
        'user': honest_user.address,
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'payment_code': actual_payment_code_the_user_got,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch(
        'webserver.payment_confirmation.redis.Redis',
    ).return_value = redis

    # Contract
    some_other_payment_code = GameInterface.new_payment_code()
    contract = mocker.patch(
        'webserver.payment_confirmation.arcade_protocol.Contract',
    ).return_value
    contract.get_payment_code.return_value = some_other_payment_code

    # Run / Test
    with pytest.raises(PaymentError):
        get_payment_confirmation(payment_locator_payload)


def test_user_no_payload(user, mocker):
    payment_locator_payload = {}

    # Run / Test
    with pytest.raises(PaymentLocatorPayloadValidationError):
        get_payment_confirmation(payment_locator_payload)


def test_user_has_no_session_id_in_redis(user, mocker):
    session_id = new_session()
    payment_locator_payload = {
        'session_id': session_id,
        'user': user.address,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch(
        'webserver.payment_confirmation.redis.Redis'
    ).return_value = redis

    # Run / Test
    with pytest.raises(UnpaidSessionValidationError):
        get_payment_confirmation(payment_locator_payload)


def test_user_has_incorrect_session(user, mocker):
    session_id = new_session()
    payment_locator_payload = {
        'session_id': session_id,
        'user': user.address,
    }

    # UnpaidSession
    unpaid_session = {}
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch(
        'webserver.payment_confirmation.redis.Redis',
    ).return_value = redis

    # Run / Test
    with pytest.raises(UnpaidSessionValidationError):
        get_payment_confirmation(payment_locator_payload)


def test_payment_doesnt_confirm(user, mocker, monkeypatch):
    payment_code = GameInterface.new_payment_code()
    session_id = new_session()
    payment_locator_payload = {
        'session_id': session_id,
        'user': user.address,
    }

    # UnpaidSession
    unpaid_session = {
        'paid': False,
        'payment_code': payment_code,
    }
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    redis.set(session_id, json.dumps(unpaid_session))
    mocker.patch(
        'webserver.payment_confirmation.redis.Redis',
    ).return_value = redis

    # Contract
    empty_payment_code = '0x0'
    contract = mocker.patch(
        'webserver.payment_confirmation.arcade_protocol.Contract',
    ).return_value
    contract.get_payment_code.return_value = empty_payment_code

    # Run
    with pytest.raises(PaymentError):
        get_payment_confirmation(payment_locator_payload)
