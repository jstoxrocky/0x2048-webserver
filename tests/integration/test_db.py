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


def test_iou_table_exists(conn):
    find_table = (
        """
        SELECT tablename
        FROM pg_catalog.pg_tables
        WHERE tablename = %(tablename)s
        ;
        """
    )
    tables = conn.execute(find_table, dict(tablename='ious')).fetchall()
    assert len(tables) == 1


def test_get_latest_nonce(mocker, conn, user):
    get_connection = mocker.patch('webserver.db.get_connection')
    get_connection.return_value.__enter__.return_value = conn
    get_connection.return_value.__exit__.return_value = None
    select_rows = (
        """
        SELECT
            nonce
        FROM ious
        WHERE user_id = %(user_id)s
        ORDER BY nonce DESC
        LIMIT 1
        ;
        """
    )
    user_id = remove_0x_prefix(user.address)
    expected, = conn.execute(select_rows, dict(user_id=user_id)).fetchone()
    nonce = get_latest_nonce(user_id)
    assert nonce == expected


def test_insert_row(mocker, conn, user):
    get_connection = mocker.patch('webserver.db.get_connection')
    get_connection.return_value.__enter__.return_value = conn
    get_connection.return_value.__exit__.return_value = None
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
        ;
        """
    )
    user_id = remove_0x_prefix(user.address)
    nonce = get_latest_nonce(user_id) + 1
    signature = remove_0x_prefix(encode_hex(
        Account.sign(b'', user.privateKey).signature
    ))
    insert_iou(nonce, user_id, signature)
    params = dict(user_id=remove_0x_prefix(user_id), nonce=nonce)
    results = conn.execute(select_rows, params).fetchall()
    assert results == [(nonce, user_id, signature)]
