import pytest
from web3 import Account
from eth_utils import (
    int_to_big_endian,
)


num_accounts = 3
accounts = []
for i in range(1, num_accounts + 1):
    pk_bytes = int_to_big_endian(i).rjust(32, b'\x00')
    account = Account.privateKeyToAccount(pk_bytes)
    accounts.append(account)


@pytest.fixture(scope="session")
def owner():
    account = accounts[0]
    return account


@pytest.fixture(scope="session")
def user():
    account = accounts[1]
    return account


@pytest.fixture(scope="session")
def user2():
    account = accounts[2]
    return account
