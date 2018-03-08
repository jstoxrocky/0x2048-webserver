# Transferred value is hardcoded in the state channel.
# A nonce is tracked in the contract.
# Only a nonce greater than the current value will be able to transfer


import os
import sqlalchemy


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


def insert_iou(conn, nonce, user_id, signature):
    insert_row = (
        """
        INSERT INTO ious (nonce, user_id, signature)
        VALUES (%(nonce)s, %(user_id)s, %(signature)s)
        ;
        """
    )
    params = dict(nonce=nonce, user_id=user_id, signature=signature)
    conn.execute(insert_row, params)


def get_latest_nonce(conn, user_id):
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
    nonce, = conn.execute(get_nonce, dict(user_id=user_id)).fetchone()
    return nonce
