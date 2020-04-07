import fakeredis
import json
from webserver.new_gamecode import (
    new_gamecode,
)
from webserver.schemas import (
    UnpaidSession,
    Gamecode,
)


def test_happy_path(mocker):
    server = fakeredis.FakeServer()
    redis = fakeredis.FakeStrictRedis(server=server)
    mocker.patch('webserver.new_gamecode.redis.Redis').return_value = redis

    gamecode_schema = json.loads(new_gamecode())
    gamecode = gamecode_schema['gamecode']
    session = json.loads(redis.get(gamecode))

    errors = UnpaidSession().validate(session)
    assert not errors
    errors = Gamecode().validate(gamecode_schema)
    assert not errors
