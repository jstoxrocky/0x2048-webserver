import pytest
from webserver.db import (
    get_engine,
)


@pytest.fixture(scope="session")
def engine():
    _engine = get_engine()
    return _engine


@pytest.fixture(scope="session")
def conn(request, engine):

    _conn = engine.connect()
    tx = _conn.begin()

    def teardown():
        tx.rollback()
        _conn.close()

    request.addfinalizer(teardown)
    return _conn
