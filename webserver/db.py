# Transferred value is hardcoded in the state channel.
# A nonce is tracked in the contract.
# Only a nonce greater than the current value will be able to transfer


import os
import sqlalchemy


HOST = os.environ['DB_0x2048_HOST']
PORT = os.environ['DB_0x2048_PORT']
USER = os.environ['DB_0x2048_USER']
PWD = os.environ['DB_0x2048_PWD']
DB = os.environ['DB_0x2048_DB']
BASE_CONN_STR = 'postgresql://{user}:{pwd}@{host}:{port}/{db}'
CONN_STR = BASE_CONN_STR.format(
    host=HOST,
    port=PORT,
    user=USER,
    pwd=PWD,
    db=DB,
)


def get_engine():
    engine = sqlalchemy.create_engine(CONN_STR)
    return engine
