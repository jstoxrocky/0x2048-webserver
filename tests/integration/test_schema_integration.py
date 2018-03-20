import os
import json
from webserver import (
    schemas,
)


this = os.path.dirname(__file__)
tests = os.path.join(this, '..')
webserver = os.path.abspath(os.path.join(tests, '..'))
integration_tests_json = os.path.join(webserver, 'integration-tests-json')
schemas_dir = os.path.join(integration_tests_json, 'schemas')


def test_user_schema():
    """
    Recevied data on GET /nonce should validate UserSchema
    """
    filepath = os.path.join(schemas_dir, "user.json")
    with open(filepath) as f:
        data = json.load(f)
    errors = schemas.UserSchema().validate(data)
    assert not errors


def test_signed_gamestate_schema():
    """
    Emitted data on GET /gamestate should validate GamestateSchema
    Emitted data on POST /move should validate GamestateSchema
    Emitted data on POST /iou should validate GamestateSchema
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


def test_iou_schema():
    """
    Recevied data on POST /iou should validate IOUSchema
    """
    filepath = os.path.join(schemas_dir, "iou.json")
    with open(filepath) as f:
        data = json.load(f)
    errors = schemas.IOUSchema().validate(data)
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
