import os
import json
from web3 import (
    Account,
)
from webserver.config import (
    PRIV,
    ARCADE_ADDR,
)


this = os.path.dirname(__file__)
tests = os.path.join(this, '..')
webserver = os.path.abspath(os.path.join(tests, '..'))
integration_json_fixtures = os.path.join(
    webserver,
    'integration-json-fixtures',
)
constants_dir = os.path.join(integration_json_fixtures, 'constants')


def test_owner():
    filepath = os.path.join(constants_dir, "address.json")
    with open(filepath) as f:
        data = json.load(f)
    assert data['owner'] == Account.privateKeyToAccount(PRIV).address


def test_arcade_contract_address():
    filepath = os.path.join(constants_dir, "address.json")
    with open(filepath) as f:
        data = json.load(f)
    assert data['arcade'] == ARCADE_ADDR
