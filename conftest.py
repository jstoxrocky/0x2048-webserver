import pytest
from web3 import Account
from eth_utils import (
    pad_left,
    int_to_big_endian,
)


num_accounts = 3
accounts = []
for i in range(1, num_accounts + 1):
    pk_bytes = pad_left(int_to_big_endian(i), 32, b'\x00')
    account = Account.privateKeyToAccount(pk_bytes)
    accounts.append(account)


@pytest.fixture(scope="module")
def owner():
    account = accounts[0]
    return account


@pytest.fixture(scope="module")
def _owner():
    account = accounts[1]
    return account


@pytest.fixture(scope="module")
def user():
    account = accounts[2]
    return account
