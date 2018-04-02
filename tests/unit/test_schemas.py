import pytest
from webserver import schemas


@pytest.mark.parametrize('key, value', [
    ('signature', 0),
])
def test_simple_signature_schema_wrong_datatype(signature_data, key, value):
    payload = {'signature': signature_data['signature']}
    payload[key] = value
    errors = schemas.SimpleSignature().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'signature',
])
def test_simple_signature_schema_missing_data(signature_data, key):
    payload = {'signature': signature_data['signature']}
    payload.pop(key)
    errors = schemas.SimpleSignature().validate(payload)
    assert len(errors) > 0


def test_simple_signature_schema_success(signature_data):
    payload = {'signature': signature_data['signature']}
    errors = schemas.SimpleSignature().validate(payload)
    assert not errors


@pytest.mark.parametrize('key, value', [
    ('message', 0),
    ('messageHash', 0),
    ('v', ''),
    ('r', 0),
    ('s', 0),
    ('signature', 0),
])
def test_full_signature_schema_wrong_datatype(signature_data, key, value):
    payload = signature_data
    payload[key] = value
    errors = schemas.FullSignature().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'message',
    'messageHash',
    'v',
    'r',
    's',
    'signature',
])
def test_full_signature_schema_missing_data(signature_data, key):
    payload = signature_data
    payload.pop(key)
    errors = schemas.FullSignature().validate(payload)
    assert len(errors) > 0


def test_full_signature_schema_success(signature_data):
    payload = signature_data
    errors = schemas.FullSignature().validate(payload)
    assert not errors


@pytest.mark.parametrize('key, value', [
    ('board', 0),
    ('score', ''),
    ('gameover', ''),
])
def test_gamestate_schema_wrong_datatype(gamestate_data, key, value):
    payload = gamestate_data
    payload[key] = value
    errors = schemas.Gamestate().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'board',
    'score',
    'gameover',
])
def test_gamestate_schema_missing_data(gamestate_data, key):
    payload = gamestate_data
    payload.pop(key)
    errors = schemas.Gamestate().validate(payload)
    assert len(errors) > 0


def test_gamestate_schema_success(gamestate_data):
    payload = gamestate_data
    errors = schemas.Gamestate().validate(payload)
    assert not errors


@pytest.mark.parametrize('key, value', [
    ('board', 0),
    ('score', ''),
    ('gameover', ''),
    ('signature', 0),
])
def test_signed_gamestate_schema_wrong_datatype(gamestate_data, key, value):
    payload = gamestate_data
    payload[key] = value
    errors = schemas.SignedGamestate().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'board',
    'score',
    'gameover',
    'signature',
])
def test_signed_gamestate_schema_missing_data(gamestate_data, key):
    payload = gamestate_data
    payload.pop(key)
    errors = schemas.SignedGamestate().validate(payload)
    assert len(errors) > 0


def test_signed_gamestate_schema_success(gamestate_data):
    payload = gamestate_data
    errors = schemas.SignedGamestate().validate(payload)
    assert not errors


@pytest.mark.parametrize('key, value', [
    ('user', 0),
    ('direction', ''),
])
def test_move_schema_wrong_datatype(move_data, key, value):
    payload = move_data
    payload[key] = value
    errors = schemas.Move().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'user',
    'direction',
])
def test_move_schema_missing_data(move_data, key):
    payload = move_data
    payload.pop(key)
    errors = schemas.Move().validate(payload)
    assert len(errors) > 0


def test_move_schema_success(move_data):
    payload = move_data
    errors = schemas.Move().validate(payload)
    assert not errors


@pytest.mark.parametrize('key, value', [
    ('nonce', 0),
])
def test_nonce_schema_wrong_datatype(nonce_data, key, value):
    payload = nonce_data
    payload[key] = value
    errors = schemas.Nonce().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'nonce',
])
def test_nonce_schema_missing_data(nonce_data, key):
    payload = nonce_data
    payload.pop(key)
    errors = schemas.Nonce().validate(payload)
    assert len(errors) > 0


def test_nonce_schema_success(nonce_data):
    payload = nonce_data
    errors = schemas.Nonce().validate(payload)
    assert not errors


@pytest.mark.parametrize('key, value', [
    ('signature', 0),
    ('txhash', 0)
])
def test_receipt_schema_wrong_datatype(receipt_data, key, value):
    payload = receipt_data
    payload[key] = value
    errors = schemas.Receipt().validate(payload)
    assert len(errors) > 0


@pytest.mark.parametrize('key', [
    'signature',
    'txhash',
])
def test_receipt_schema_missing_data(receipt_data, key):
    payload = receipt_data
    payload.pop(key)
    errors = schemas.Receipt().validate(payload)
    assert len(errors) > 0


def test_receipt_schema_success(receipt_data):
    payload = receipt_data
    errors = schemas.Receipt().validate(payload)
    assert not errors
