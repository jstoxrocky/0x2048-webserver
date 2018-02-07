from web3 import (
    Account,
)
from webserver.config import (
    PRIV,
)


def test_owner():
    owner_addr = '0x768Cd761C8809E2112F67767D76De3a4E6e5133D'
    assert owner_addr == Account.privateKeyToAccount(PRIV).address
