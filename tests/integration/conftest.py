import pytest
import os
import sqlalchemy
from web3 import (
    Account,
)
from eth_utils import (
    remove_0x_prefix,
    encode_hex,
)


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


@pytest.fixture(scope="session", autouse=True)
def create_iou_table(conn):
    # TODO user_id to address
    # """
    #     CREATE TABLE ious (
    #       address char(40),
    #       nonce integer CONSTRAINT positive_nonce CHECK (nonce > 0),
    #       PRIMARY KEY (user_id, nonce)
    #     )
    # ;
    # """
    create_table = (
        """
        CREATE TABLE ious (
          user_id char(40),
          nonce integer CONSTRAINT positive_nonce CHECK (nonce > 0),
          signature char(130) NOT NULL,
          finalized boolean DEFAULT FALSE NOT NULL,
          PRIMARY KEY (user_id, nonce)
        )
        ;
        """
    )
    conn.execute(create_table)


@pytest.fixture(scope="session", autouse=True)
def populate_iou_table(conn, user, user2):
    insert_row = (
        """
        INSERT INTO ious (nonce, user_id, signature)
        VALUES (%(nonce)s, %(user_id)s, %(signature)s)
        ;
        """
    )
    for _user in [user, user2]:
        for i in range(1, 11):
            nonce = i
            user_id = remove_0x_prefix(_user.address)
            signature = remove_0x_prefix(
                encode_hex(Account.sign(b'', _user.privateKey).signature)
            )
            params = dict(nonce=nonce, user_id=user_id, signature=signature)
            conn.execute(insert_row, params)
