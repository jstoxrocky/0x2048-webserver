import fakeredis
import json
from webserver.new_session import (
    new_session,
)
from webserver.schemas import (
    UnpaidSession,
    Challenge,
)


def test_happy_path(mocker):
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.new_session.redis.Redis').return_value = redis

    event, context = None, None
    challenge = json.loads(new_session(event, context))
    session_id = challenge['session_id']
    session = json.loads(redis.get(session_id))

    errors = UnpaidSession().validate(session)
    assert not errors
    errors = Challenge().validate(challenge)
    assert not errors
