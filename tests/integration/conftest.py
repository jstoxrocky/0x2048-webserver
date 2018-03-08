import pytest
import os
import sqlalchemy


@pytest.fixture(scope="session")
def engine():
    host = os.environ['DB_0x2048_HOST']
    port = os.environ['DB_0x2048_PORT']
    user = os.environ['DB_0x2048_USER']
    pwd = os.environ['DB_0x2048_PWD']
    db = os.environ['DB_TEST_0x2048_DB']
    base_conn_str = 'postgresql://{user}:{pwd}@{host}:{port}/{db}'
    conn_str = base_conn_str.format(
        host=host,
        port=port,
        user=user,
        pwd=pwd,
        db=db,
    )
    engine = sqlalchemy.create_engine(conn_str)
    return engine


@pytest.fixture(scope="session")
def conn(request, engine):

    _conn = engine.connect()
    tx = _conn.begin()

    def teardown():
        tx.rollback()
        _conn.close()

    request.addfinalizer(teardown)
    return _conn
