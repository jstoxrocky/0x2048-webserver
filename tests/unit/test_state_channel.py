import pytest
from webserver.state_channel import (
    sign,
    recover,
    int_to_hex,
    solidity_keccak,
    validate_iou,
    raw_sign,
    hash_typed_data,
    sign_typed_data,
)
from webserver.config import (
    PRIV,
    ARCADE_ADDR,
    ACCOUNT_ADDR,
    DISCLAIMER,
)
from web3 import (
    Account,
)


def test_sign(user):
    msg = solidity_keccak(ARCADE_ADDR, user.address, 1, 2, 3)
    output = sign(msg, PRIV)
    assert isinstance(output['r'], str)
    assert isinstance(output['s'], str)


def test_raw_sign(user):
    msg = b'Joey to the world!'
    signature = raw_sign(msg, user.privateKey)
    assert signature.to_hex() == '0xc940c68a311665c9329c22e3b858bcb91f9c7dc95844c61401ad61f28ba5274e7b1b5d673f6e9494df2fa1d586d49add102f736ac02cc28e6aff221e0fc09a5901'  # noqa: E501


def test_int_to_hex():
    assert len(int_to_hex(16**0)) % 2 == 0
    assert len(int_to_hex(16**1)) % 2 == 0
    assert len(int_to_hex(16**2)) % 2 == 0


def test_recover(user):
    msg = solidity_keccak(ARCADE_ADDR, user.address, 1, 2, 3)
    signed = Account.sign(msg, user.privateKey)
    signer = recover(signed['messageHash'], signed['signature'])
    assert signer == user.address


def test_solidity_keccak(user):
    value = 1
    msg = solidity_keccak(user.address, user.address, value)
    print(msg)
    assert msg == b'g\xd5\x0c\x96A\xb5\xcbJ\xe4]{\x8c\x00\xd0\x8c\x1b\r\xb9>6\xb2j\xe7\x80@\xf9\x11\x14\x93!\xb7\x81'  # noqa: E501


def test_validate_iou(user):
    nonce = 1
    msg_params = [
        {'type': 'string', 'name': DISCLAIMER, 'value': ACCOUNT_ADDR},
        {'type': 'address', 'name': 'user', 'value': user.address},
        {'type': 'uint256', 'name': 'nonce', 'value': nonce},
    ]
    signature = sign_typed_data(msg_params, user.privateKey)
    iou = {
        'user': user.address,
        'nonce': nonce,
        'signature': signature,
    }
    success = validate_iou(iou)
    assert success


@pytest.mark.parametrize('key, test_value', [
    ('nonce', 1337),
    ('user', '0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69'),  # user2.address
])
def test_validate_iou_bad_preimage(user, key, test_value):
    nonce = 1
    msg_params = [
        {'type': 'string', 'name': DISCLAIMER, 'value': ACCOUNT_ADDR},
        {'type': 'address', 'name': 'user', 'value': user.address},
        {'type': 'uint256', 'name': 'nonce', 'value': nonce},
    ]
    signature = sign_typed_data(msg_params, user.privateKey)
    iou = {
        'user': user.address,
        'nonce': nonce,
        'signature': signature,
    }
    iou[key] = test_value
    success = validate_iou(iou)
    assert not success


def test_validate_iou_bad_signer(user, user2):
    nonce = 1
    msg_params = [
        {'type': 'string', 'name': DISCLAIMER, 'value': ACCOUNT_ADDR},
        {'type': 'address', 'name': 'user', 'value': user2.address},
        {'type': 'uint256', 'name': 'nonce', 'value': nonce},
    ]
    signature = sign_typed_data(msg_params, user2.privateKey)
    iou = {
        'user': user.address,
        'nonce': nonce,
        'signature': signature,
    }
    success = validate_iou(iou)
    assert not success


def test_sign_typed_data(user):
    msg_params = [
        {'type': 'uint256', 'name': 'x', 'value': 1},
    ]
    msg_hash = hash_typed_data(msg_params)
    signature = sign_typed_data(msg_params, user.privateKey)
    signer = recover(msg_hash, signature)
    assert signer == user.address
