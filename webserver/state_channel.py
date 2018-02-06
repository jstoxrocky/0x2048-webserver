from web3 import (
    Web3,
    Account,
)
from toolz.dicttoolz import (
    valmap,
)
from eth_utils import (
    encode_hex,
    int_to_big_endian,
)


def int_to_hex(integer):
    return encode_hex(int_to_big_endian(integer))


def sign(private_key, contract, user, *values):
    abi_types = ['address', 'address'] + ['uint256'] * len(values)
    msg = Web3.soliditySha3(abi_types, [contract, user] + list(values))
    signed = Account.sign(msg, private_key)
    signed = valmap(lambda x: x.hex() if isinstance(x, bytes) else x, signed)
    signed['r'] = int_to_hex(signed['r'])
    signed['s'] = int_to_hex(signed['s'])
    return signed
