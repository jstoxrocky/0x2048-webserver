from webserver.state_channel import (
    sign,
)
from webserver.config import (
    PRIV,
    ADDR,
)


def test_sign(user):
    expected_output = {'message': '0xa36960f19a100a346e83a809b03f94eb7c2c862987c1a95f92d9b93e383b6983', 'messageHash': '0x80ea0172ca9ffad1b0ee4a4df65b39e6259057654a16545626653582be155598', 'r': '0x9542b6b9fcce18421cad27784845931e3a332b103b534a5ea5a5014d51949095', 's': '0x1907c27fef888222a5b22bdc1addc5e7bb5c120cbc130de8000f6058192d18f7', 'v': 28, 'signature': '0x9542b6b9fcce18421cad27784845931e3a332b103b534a5ea5a5014d519490951907c27fef888222a5b22bdc1addc5e7bb5c120cbc130de8000f6058192d18f71c'}  # noqa: 501
    output = sign(PRIV, ADDR, user, 1, 2, 3)
    assert output == expected_output
