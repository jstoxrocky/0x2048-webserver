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
from webserver.config import (
    ACCOUNT_ADDR,
)


def int_to_hex(integer):
    return encode_hex(int_to_big_endian(integer))


def solidity_keccak(contract, user, *values):
    abi_types = ['address', 'address'] + ['uint256'] * len(values)
    msg = Web3.soliditySha3(abi_types, [contract, user] + list(values))
    return msg


def sign(msg, private_key):
    signed = Account.sign(msg, private_key)
    signed = valmap(lambda x: x.hex() if isinstance(x, bytes) else x, signed)
    signed['r'] = int_to_hex(signed['r'])
    signed['s'] = int_to_hex(signed['s'])
    return signed


def recover(signed):
    signer = Account.recover(
        signed['messageHash'],
        signature=signed['signature'],
    )
    return signer


def validate_iou(iou):
    # Do the preimages hash together to form the signed message
    expected_msg = solidity_keccak(
        ACCOUNT_ADDR,
        iou['user'],
        iou['value'],
    )
    if expected_msg.hex() != iou['signature']['message']:
        return False
    # Does the message signer match the user preimage
    if recover(iou['signature']) != iou['user']:
        return False
    return True
