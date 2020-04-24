import os
from hexbytes import (
    HexBytes,
)


def new_session():
    session_id = HexBytes(os.urandom(32)).hex()
    return session_id
