import fakeredis
import json
from webserver.gamecode import (
    gamecode as get_gamecode,
)
from webserver.schemas import (
    UnpaidSession,
    Gamecode,
)


def test_happy_path(mocker):
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.gamecode.redis.Redis').return_value = redis

    gamecode = json.loads(get_gamecode())
    session_id = gamecode['session_id']
    session = json.loads(redis.get(session_id))

    errors = UnpaidSession().validate(session)
    assert not errors
    errors = Gamecode().validate(gamecode)
    assert not errors
