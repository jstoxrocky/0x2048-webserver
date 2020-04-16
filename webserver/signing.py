import os
from web3 import (
    Account,
)
from hexbytes import (
    HexBytes,
)
from webserver.config import (
    ARCADE_ADDRESS,
    PRIV,
)
from eth_account.messages import (
    encode_intended_validator,
)
from eth_abi.packed import (
    encode_abi_packed,
)


def sign_score(game_id, user, score):
    game_id = HexBytes(game_id)
    types = ['bytes32', 'address', 'uint256']
    values = [game_id, user, score]
    encoded_values = encode_abi_packed(types, values)
    message = encode_intended_validator(
        validator_address=ARCADE_ADDRESS,
        primitive=encoded_values,
    )
    signed = Account.sign_message(message, PRIV)
    vrs = (
        signed['v'],
        HexBytes(signed['r']).hex(),
        HexBytes(signed['s']).hex(),
    )
    return vrs


def random_32bytes():
    value = HexBytes(os.urandom(32))
    return value.hex()
