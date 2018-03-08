from web3 import (
    Account,
)
from eth_utils import (
    remove_0x_prefix,
    encode_hex,
)
from webserver.db import (
    insert_iou,
    get_latest_nonce,
)


def test_create_table(conn):
    create_table = (
        """
        CREATE TABLE ious (
          user_id char(40),
          nonce integer CONSTRAINT positive_nonce CHECK (nonce > 0),
          signature char(130) NOT NULL,
          PRIMARY KEY (user_id, nonce)
        )
        ;
        """
    )
    find_table = (
        """
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE tablename = %(tablename)s
        ;
        """
    )
    conn.execute(create_table)
    tables = conn.execute(find_table, dict(tablename='ious')).fetchall()
    assert len(tables) == 1


def test_insert_row(mocker, conn, user):
    select_rows = (
        """
        SELECT
            nonce,
            user_id,
            signature
        FROM ious
        WHERE TRUE
          AND user_id = %(user_id)s
          AND nonce = %(nonce)s
        LIMIT 10
        ;
        """
    )
    nonce = 1
    user_id = remove_0x_prefix(user.address)
    signature = remove_0x_prefix(
        encode_hex(Account.sign(b'', user.privateKey).signature)
    )
    insert_iou(conn, nonce, user_id, signature)
    params = dict(user_id=user_id, nonce=nonce)
    results = conn.execute(select_rows, params).fetchall()
    assert results == [(nonce, user_id, signature)]


def test_get_latest_nonce(conn, user):
    user_id = remove_0x_prefix(user.address)
    nonce = get_latest_nonce(conn, user_id)
    assert nonce == 1
