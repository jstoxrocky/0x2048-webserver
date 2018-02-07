from webserver.state_channel import (
    sign,
    int_to_hex,
)
from webserver.config import (
    PRIV,
    ADDR,
)


def test_sign(user):
    output = sign(PRIV, ADDR, user, 1, 2, 3)
    assert isinstance(output['r'], str)
    assert isinstance(output['s'], str)


def test_int_to_hex():
    assert len(int_to_hex(16**0)) % 2 == 0
    assert len(int_to_hex(16**1)) % 2 == 0
    assert len(int_to_hex(16**2)) % 2 == 0
