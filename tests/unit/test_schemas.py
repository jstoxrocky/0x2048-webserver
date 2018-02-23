import pytest
from webserver.schemas import (
    SignatureSchema,
    IOUSchema,
    GamestateSchema,
    MoveSchema,
)


@pytest.mark.parametrize('key, value', [
    ('message', 0),
    ('messageHash', 0),
    ('v', ''),
    ('r', 0),
    ('s', 0),
    ('signature', 0),
])
def test_signature_schema_wrong_datatype(iou_data, key, value):
    payload = iou_data['signature']
    payload[key] = value
    errors = SignatureSchema().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'message',
    'messageHash',
    'v',
    'r',
    's',
    'signature',
])
def test_signature_schema_missing_data(iou_data, key):
    payload = iou_data['signature']
    payload.pop(key)
    errors = SignatureSchema().validate(payload)
    print(errors)
    assert len(errors) > 0


def test_signature_schema_success(iou_data):
    payload = iou_data['signature']
    errors = SignatureSchema().validate(payload)
    assert not errors


@pytest.mark.parametrize('key, value', [
    ('user', 0),
    ('value', ''),
    ('signature', 0),
])
def test_iou_schema_wrong_datatype(iou_data, key, value):
    payload = iou_data
    payload[key] = value
    errors = IOUSchema().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'user',
    'value',
    'signature',
])
def test_iou_schema_missing_data(iou_data, key):
    payload = iou_data
    payload.pop(key)
    errors = IOUSchema().validate(payload)
    assert len(errors) > 0


def test_iou_schema_success(iou_data):
    payload = iou_data
    errors = IOUSchema().validate(payload)
    assert not errors


@pytest.mark.parametrize('key, value', [
    ('board', 0),
    ('score', ''),
    ('gameover', ''),
    ('signature', 0),
])
def test_gamestate_schema_wrong_datatype(gamestate_data, key, value):
    payload = gamestate_data
    payload[key] = value
    errors = GamestateSchema().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'board',
    'score',
    'gameover',
    'signature',
])
def test_gamestate_schema_missing_data(gamestate_data, key):
    payload = gamestate_data
    payload.pop(key)
    errors = GamestateSchema().validate(payload)
    assert len(errors) > 0


def test_gamestate_schema_success(gamestate_data):
    payload = gamestate_data
    errors = GamestateSchema().validate(payload)
    assert not errors


@pytest.mark.parametrize('key, value', [
    ('user', 0),
    ('direction', ''),
])
def test_move_schema_wrong_datatype(move_data, key, value):
    payload = move_data
    payload[key] = value
    errors = MoveSchema().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'user',
    'direction',
])
def test_move_schema_missing_data(move_data, key):
    payload = move_data
    payload.pop(key)
    errors = MoveSchema().validate(payload)
    assert len(errors) > 0


def test_move_schema_success(move_data):
    payload = move_data
    errors = MoveSchema().validate(payload)
    assert not errors
