import os
import json
from webserver import (
    schemas,
)


this_dir = os.path.dirname(__file__)
test_dir = os.path.join(this_dir, '..')
project_dir = os.path.join(test_dir, '..')
abs_path_to_project_dir = os.path.abspath(project_dir)
schema_integration_test_dir = os.path.join(
    abs_path_to_project_dir, 'schema-integration-tests'
)


def test_user_schema():
    """
    Recevied data on GET /gamestate should validate UserSchema
    Recevied data on GET /nonce should validate UserSchema
    """
    filepath = os.path.join(schema_integration_test_dir, "user.json")
    with open(filepath) as f:
        data = json.load(f)
    errors = schemas.UserSchema().validate(data)
    assert not errors


def test_gamestate_schema():
    """
    Emitted data on GET /gamestate should validate GamestateSchema
    Emitted data on POST /move should validate GamestateSchema
    Emitted data on POST /iou should validate GamestateSchema
    """
    filepath = os.path.join(schema_integration_test_dir, "gamestate.json")
    with open(filepath) as f:
        data = json.load(f)
    errors = schemas.GamestateSchema().validate(data)
    assert not errors


def test_move_schema():
    """
    Recevied data on POST /move should validate MoveSchema
    """
    filepath = os.path.join(schema_integration_test_dir, "move.json")
    with open(filepath) as f:
        data = json.load(f)
    errors = schemas.MoveSchema().validate(data)
    assert not errors


def test_iou_schema():
    """
    Recevied data on POST /iou should validate IOUSchema
    """
    filepath = os.path.join(schema_integration_test_dir, "iou.json")
    with open(filepath) as f:
        data = json.load(f)
    errors = schemas.IOUSchema().validate(data)
    assert not errors


def test_nonce_schema():
    """
    Emitted data on GET /nonce should validate NonceSchema
    """
    filepath = os.path.join(schema_integration_test_dir, "nonce.json")
    with open(filepath) as f:
        data = json.load(f)
    errors = schemas.NonceSchema().validate(data)
    assert not errors
