import os
import sqlalchemy
from eth_utils import (
    remove_0x_prefix,
)


def get_engine():
    host = os.environ['DB_0x2048_HOST']
    port = os.environ['DB_0x2048_PORT']
    user = os.environ['DB_0x2048_USER']
    pwd = os.environ['DB_0x2048_PWD']
    db = os.environ['DB_0x2048_DB']
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


def get_connection():
    engine = get_engine()
    return engine.connect()


def insert_iou(nonce, user, signature):
    insert_row = (
        """
        INSERT INTO ious (nonce, user_id, signature)
        VALUES (%(nonce)s, %(user_id)s, %(signature)s)
        ;
        """
    )
    user_id = remove_0x_prefix(user)
    signature = remove_0x_prefix(signature)
    params = dict(nonce=nonce, user_id=user_id, signature=signature)
    with get_connection() as conn:
        conn.execute(insert_row, params)


def get_latest_nonce(user_id):
    get_nonce = (
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
    user_id = remove_0x_prefix(user_id)
    with get_connection() as conn:
        result = conn.execute(get_nonce, dict(user_id=user_id)).fetchone()
        result = result or (0,)
        nonce, = result
    return nonce


def sum_outstanding_ious(user_id):
    count_outstanding = (
        """
        SELECT
          COUNT(nonce) AS count_outstanding
        FROM ious
        WHERE TRUE
          AND ious.user_id = %(user_id)s
          AND NOT finalized
        """
    )
    user_id = remove_0x_prefix(user_id)
    with get_connection() as conn:
        params = dict(user_id=user_id)
        result = conn.execute(count_outstanding, params).fetchone()
        result = result or (0,)
        nonce, = result
    return nonce
