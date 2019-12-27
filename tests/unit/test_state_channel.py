from webserver.state_channel import (
    sign,
    recover,
    int_to_hex,
    solidity_keccak,
    raw_sign,
    hash_typed_data,
    sign_typed_data,
    generate_random_nonce,
    prepare_messageHash_for_signing,
)
from webserver.config import (
    PRIV,
    ARCADE_ADDRESS,
)
from web3 import (
    Account,
)
from eth_utils import (
    decode_hex,
)


def test_sign(user):
    msg = solidity_keccak(ARCADE_ADDRESS, user.address, 1, 2, 3)
    output = sign(msg, PRIV)
    assert isinstance(output['r'], str)
    assert isinstance(output['s'], str)
    signer = recover(
        output['messageHash'],
        output['signature'],
    )
    owner = Account.privateKeyToAccount(PRIV).address
    assert signer == owner


def test_raw_sign(user):
    msg = b'Joey to the world!'
    signature = raw_sign(msg, user.privateKey)
    assert signature.to_hex() == '0xc940c68a311665c9329c22e3b858bcb91f9c7dc95844c61401ad61f28ba5274e7b1b5d673f6e9494df2fa1d586d49add102f736ac02cc28e6aff221e0fc09a5901'  # noqa: E501


def test_int_to_hex():
    assert len(int_to_hex(16**0)) % 2 == 0
    assert len(int_to_hex(16**1)) % 2 == 0
    assert len(int_to_hex(16**2)) % 2 == 0


def test_recover(user):
    msg = solidity_keccak(ARCADE_ADDRESS, user.address, 1, 2, 3)
    signed = Account.signHash(msg, user.privateKey)
    signer = recover(signed['messageHash'], signed['signature'])
    assert signer == user.address


def test_solidity_keccak(user):
    value = 1
    msg = solidity_keccak(user.address, user.address, value)
    assert msg == b'g\xd5\x0c\x96A\xb5\xcbJ\xe4]{\x8c\x00\xd0\x8c\x1b\r\xb9>6\xb2j\xe7\x80@\xf9\x11\x14\x93!\xb7\x81'  # noqa: E501


def test_sign_typed_data(user):
    msg_params = [
        {'type': 'uint256', 'name': 'x', 'value': 1},
    ]
    msg_hash = hash_typed_data(msg_params)
    signature = sign_typed_data(msg_params, user.privateKey)
    signer = recover(msg_hash, signature)
    assert signer == user.address


def test_generate_random_nonce():
    nonce = generate_random_nonce()
    assert len(decode_hex(nonce)) == 32


def test_prepare_messageHash_for_signing(mocker):
    mock_addr = '0xA393E5Af104919f023ce0b6d0E5adD1CeDD0120C'
    mocker.patch('webserver.state_channel.ARCADE_ADDRESS', mock_addr)
    nonce = '0x01'
    msgHash = prepare_messageHash_for_signing(nonce)
    assert msgHash == b'5-\xa3<G?\xc8\x08\r4\x1f\xda\xa8f\x90\x1c\xe5`\xaad\xac\x88\x10\x11B,\xc6,\xce-Y\xa9'  # noqa: E501
