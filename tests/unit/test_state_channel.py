from webserver.state_channel import (
    sign,
    recover,
    int_to_hex,
    solidityKeccak,
)
from webserver.config import (
    PRIV,
    ARCADE_ADDR,
)
from web3 import (
    Account,
)


def test_sign(user):
    msg = solidityKeccak(ARCADE_ADDR, user.address, 1, 2, 3)
    output = sign(msg, PRIV)
    assert isinstance(output['r'], str)
    assert isinstance(output['s'], str)


def test_int_to_hex():
    assert len(int_to_hex(16**0)) % 2 == 0
    assert len(int_to_hex(16**1)) % 2 == 0
    assert len(int_to_hex(16**2)) % 2 == 0


def test_recover(user):
    msg = b'Joey to the world!'
    signed = Account.sign(msg, user.privateKey)
    signer = recover(signed)
    assert signer == user.address


def test_solidityKeccak(user):
    contract = ARCADE_ADDR
    value = 1
    msg = solidityKeccak(contract, user.address, value)
    assert msg == b'\xb7\xeaz\r:\x96\xd1\xd3\xda}\x9cI\x8c\xd1\xae\x02x\x05a0\xd4+\xbb\xce\xaf\xfd\xcd\x13$\xf2\xa7\xbe'  # noqa: E501
