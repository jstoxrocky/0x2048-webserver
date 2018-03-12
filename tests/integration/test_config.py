import os
import json
from web3 import (
    Account,
)
from webserver.config import (
    PRIV,
)


this = os.path.dirname(__file__)
tests = os.path.join(this, '..')
webserver = os.path.abspath(os.path.join(tests, '..'))
integration_tests_json = os.path.join(webserver, 'integration-tests-json')
constants_dir = os.path.join(integration_tests_json, 'constants')


def test_owner():
    filepath = os.path.join(constants_dir, "address.json")
    with open(filepath) as f:
        data = json.load(f)
    assert data['owner'] == Account.privateKeyToAccount(PRIV).address
