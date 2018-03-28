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
    to_bytes,
    keccak,
)
from webserver.config import (
    ARCADE_ADDR,
    DISCLAIMER,
)
from eth_keys import (
    keys,
)
from eth_account.signing import (
    to_eth_v,
    to_bytes32,
)
import os


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


def recover(msg, signature):
    signer = Account.recover(
        msghash=msg,
        signature=signature,
    )
    return signer


def raw_sign(msg_hash, private_key):
    key = keys.PrivateKey(private_key)
    raw_signature = key.sign_msg_hash(msg_hash)
    return raw_signature


def hash_typed_data(msg_params):
    data = list(map(lambda x: x['value'], msg_params))
    types = list(map(lambda x: x['type'], msg_params))
    schema = list(map(lambda x: ' '.join([x['type'], x['name']]), msg_params))
    msg_hash = Web3.soliditySha3(
        ['bytes32', 'bytes32'],
        [
            Web3.soliditySha3(['string'] * len(msg_params), schema),
            Web3.soliditySha3(types, data),
        ]
    )
    return msg_hash


def sign_typed_data(msg_params, private_key):
    msg_hash = hash_typed_data(msg_params)
    key = keys.PrivateKey(private_key)
    raw_signature = key.sign_msg_hash(msg_hash)
    v_raw, r, s = raw_signature.vrs
    v = to_eth_v(v_raw)
    signature = encode_hex(to_bytes32(r) + to_bytes32(s) + to_bytes(v))
    return signature


def validate_iou(iou):
    msg_params = [
        {'type': 'string', 'name': DISCLAIMER, 'value': ARCADE_ADDR},
        {'type': 'address', 'name': 'user', 'value': iou['user']},
        {'type': 'uint256', 'name': 'nonce', 'value': iou['nonce']},
    ]
    msg_hash = hash_typed_data(msg_params)
    if recover(msg_hash, iou['signature']) != iou['user']:
        return False
    return True


def generate_random_nonce():
    nonce = os.urandom(32)
    return encode_hex(nonce)


def prepare_messageHash_for_signing(msg):
    return keccak(msg)
