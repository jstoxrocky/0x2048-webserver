from web3 import (
    Web3,
    Account,
)
from toolz.dicttoolz import (
    valmap,
)


def sign(private_key, contract, user, *values):
    abi_types = ['address', 'address'] + ['uint256'] * len(values)
    msg = Web3.soliditySha3(abi_types, [contract, user] + list(values))
    signed = Account.sign(msg, private_key)
    signed = valmap(lambda x: x.hex() if isinstance(x, bytes) else x, signed)
    return signed
