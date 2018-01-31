import pytest
from eth_utils import (
    to_checksum_address,
    keccak,
)
from ethereum.keys import (
    privtoaddr,
)


@pytest.fixture(scope="module")
def owner_priv():
    return b'\x11' * 32


@pytest.fixture(scope="module")
def _owner_priv():
    return keccak('3')


@pytest.fixture(scope="module")
def owner():
    return to_checksum_address(privtoaddr(b'\x11' * 32))


@pytest.fixture(scope="module")
def user():
    return to_checksum_address(privtoaddr(keccak('2')))
