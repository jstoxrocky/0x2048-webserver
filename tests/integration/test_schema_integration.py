import os
import json
from webserver import (
    schemas,
)


this = os.path.dirname(__file__)
tests = os.path.join(this, '..')
webserver = os.path.abspath(os.path.join(tests, '..'))
integration_json_fixtures = os.path.join(
    webserver,
    'integration-json-fixtures',
)
schemas_dir = os.path.join(integration_json_fixtures, 'schemas')


def test_signed_gamestate_schema():
    """
    Emitted data on GET /gamestate should validate GamestateSchema
    Emitted data on POST /move should validate GamestateSchema
    Emitted data on GET /payment-confirmation should validate GamestateSchema
    """
    filepath = os.path.join(schemas_dir, "signed-gamestate.json")  # noqa: E501
    with open(filepath) as f:
        data = json.load(f)
    errors = schemas.SignedGamestateSchema().validate(data)
    assert not errors


def test_move_schema():
    """
    Recevied data on POST /move should validate MoveSchema
    """
    filepath = os.path.join(schemas_dir, "move.json")
    with open(filepath) as f:
        data = json.load(f)
    errors = schemas.MoveSchema().validate(data)
    assert not errors


def test_nonce_schema():
    """
    Emitted data on GET /nonce should validate NonceSchema
    """
    filepath = os.path.join(schemas_dir, "nonce.json")
    with open(filepath) as f:
        data = json.load(f)
    errors = schemas.NonceSchema().validate(data)
    assert not errors
