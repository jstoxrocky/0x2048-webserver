import os
import json
from webserver.contract import (
    contract,
)


this = os.path.dirname(__file__)
tests = os.path.join(this, '..')
webserver = os.path.abspath(os.path.join(tests, '..'))
integration_tests_json = os.path.join(webserver, 'integration-tests-json')
constants_dir = os.path.join(integration_tests_json, 'constants')


def test_contract_address_matches_integration_json():
    filepath = os.path.join(constants_dir, "address.json")
    with open(filepath) as f:
        data = json.load(f)
    assert data['account'] == contract.address


def test_contract_abi_matches_integration_json():
    filepath = os.path.join(constants_dir, "abi.json")
    with open(filepath) as f:
        data = json.load(f)
    assert data['account'] == contract.abi
