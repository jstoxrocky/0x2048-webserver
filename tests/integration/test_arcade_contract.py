import os
import json
from webserver.contract import (
    contract,
)


this = os.path.dirname(__file__)
tests = os.path.join(this, '..')
webserver = os.path.abspath(os.path.join(tests, '..'))
integration_json_fixtures = os.path.join(
    webserver,
    'integration-json-fixtures',
)
constants_dir = os.path.join(integration_json_fixtures, 'constants')


def test_contract_address_matches_integration_json():
    filepath = os.path.join(constants_dir, "address.json")
    with open(filepath) as f:
        data = json.load(f)
    assert data['arcade'] == contract.address


def test_contract_abi_matches_integration_json():
    filepath = os.path.join(constants_dir, "abi.json")
    with open(filepath) as f:
        data = json.load(f)
    assert data['arcade'] == contract.abi
