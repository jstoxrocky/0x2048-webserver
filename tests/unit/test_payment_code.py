import fakeredis
import json
from webserver.payment_code import (
    payment_code as get_payment_code,
)
from webserver.schemas import (
    UnpaidSession,
    PaymentCodeResponse,
)


def test_happy_path(mocker):
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.payment_code.redis.Redis').return_value = redis

    payment_code = json.loads(get_payment_code())
    session_id = payment_code['session_id']
    session = json.loads(redis.get(session_id))

    errors = UnpaidSession().validate(session)
    assert not errors
    errors = PaymentCodeResponse().validate(payment_code)
    assert not errors
