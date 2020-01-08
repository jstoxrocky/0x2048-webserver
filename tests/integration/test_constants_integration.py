import os
import json
from web3 import (
    Account,
)
from webserver.config import (
    PRIV,
)
from webserver.config import (
    ARCADE_ADDRESS,
    ARCADE_ABI,
)


this = os.path.dirname(__file__)
tests = os.path.join(this, '..')
webserver = os.path.abspath(os.path.join(tests, '..'))
integration_json_fixtures = os.path.join(
    webserver,
    'integration-json-fixtures',
)
constants_dir = os.path.join(integration_json_fixtures, 'constants')


def test_owner_address_matches_json_fixture():
    filepath = os.path.join(constants_dir, "address.json")
    with open(filepath) as f:
        data = json.load(f)
    assert data['owner'] == Account.from_key(PRIV).address


def test_contract_address_matches_json_fixture():
    filepath = os.path.join(constants_dir, "address.json")
    with open(filepath) as f:
        data = json.load(f)
    assert data['arcade'] == ARCADE_ADDRESS


def test_contract_abi_matches_json_fixture():
    filepath = os.path.join(constants_dir, "abi.json")
    with open(filepath) as f:
        data = json.load(f)
    assert data['arcade'] == json.loads(ARCADE_ABI)
