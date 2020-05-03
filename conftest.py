import pytest
from web3 import Account
from eth_utils import (
    int_to_big_endian,
)


num_accounts = 3
accounts = []
for i in range(1, num_accounts + 1):
    pk_bytes = int_to_big_endian(i).rjust(32, b'\x00')
    account = Account.from_key(pk_bytes)
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


class MockContract():

    @staticmethod
    def get_highscore():
        return 17

    @staticmethod
    def get_price():
        return 1000000000000000

    @staticmethod
    def get_jackpot():
        return 4000000000000000


@pytest.fixture(scope="session")
def mock_contract():
    return MockContract
