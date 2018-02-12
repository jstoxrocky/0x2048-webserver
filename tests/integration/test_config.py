from web3 import (
    Account,
)
from webserver.config import (
    PRIV,
)


def test_owner():
    owner_addr = '0x60Bb3F9D894Bd74e72c3F90FA1A50Ea915a60260'
    assert owner_addr == Account.privateKeyToAccount(PRIV).address
