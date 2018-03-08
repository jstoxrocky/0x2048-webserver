from web3 import (
    Account,
)
from eth_utils import (
    remove_0x_prefix,
    encode_hex,
)


def test_create_table(conn):
    create_table = (
        """
        CREATE TABLE ious (
          pk_id serial NOT NULL,
          nonce integer NOT NULL,
          user_id char(40) NOT NULL,
          signature char(130) NOT NULL
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


def test_insert_row(conn, user):
    insert_row = (
        """
        INSERT INTO ious (nonce, user_id, signature)
        VALUES (%(nonce)s, %(user_id)s, %(signature)s)
        ;
        """
    )
    select_rows = (
        """
        SELECT
            nonce,
            user_id,
            signature
        FROM ious
        LIMIT 10
        ;
        """
    )
    signature = remove_0x_prefix(
        encode_hex(Account.sign(b'', user.privateKey).signature)
    )
    params = {
        'nonce': 1,
        'user_id': remove_0x_prefix(user.address),
        'signature': signature,
    }
    conn.execute(insert_row, params)
    results = conn.execute(select_rows).fetchall()
    assert len(results) == 1


def test_retrieve_nonce(conn, user):
    retrieve_nonce = (
        """
        SELECT
          ious.nonce
        FROM ious
        INNER JOIN (
          SELECT
            max(ious.nonce) AS nonce,
            ious.user_id AS user_id
          FROM ious
          WHERE ious.user_id = %(user_id)s
          GROUP BY user_id
        ) AS this
        ON ious.nonce = this.nonce
        AND ious.user_id = this.user_id
        ;
        """
    )
    user_id = remove_0x_prefix(user.address)
    result, = conn.execute(retrieve_nonce, dict(user_id=user_id)).fetchone()
    assert result == 1
