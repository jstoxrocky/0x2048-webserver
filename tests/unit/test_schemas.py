from webserver import (
    schemas,
)


def test_code_schema_wrong_datatype():
    payload = {'code': 1}
    errors = schemas.Code().validate(payload)
    assert len(errors) > 0


def test_code_schema_missing_data():
    payload = {}
    errors = schemas.Code().validate(payload)
    assert len(errors) > 0


def test_code_schema_hex_not_32_bytes():
    code = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca'
    payload = {
        'code': code,
    }
    errors = schemas.Code().validate(payload)
    assert len(errors) > 0


def test_code_schema_success():
    code = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4d'  # noqa: E501
    payload = {
        'code': code,
    }
    errors = schemas.Code().validate(payload)
    assert not errors


def test_address_schema_wrong_datatype():
    payload = {'address': 1}
    errors = schemas.Address().validate(payload)
    assert len(errors) > 0


def test_address_schema_missing_data():
    payload = {}
    errors = schemas.Address().validate(payload)
    assert len(errors) > 0


def test_address_not_20_bytes(user):
    address = '0x2B5AD5c4795c026514f8317c7a215E218DcCD6'
    payload = {
        'address': address,
    }
    errors = schemas.Address().validate(payload)
    assert len(errors) > 0


def test_address_schema_success(user):
    address = user.address
    payload = {
        'address': address,
    }
    errors = schemas.Address().validate(payload)
    assert not errors


def test_gamecode_schema_wrong_datatype():
    gamecode = 1
    payload = {
        'gamecode': gamecode
    }
    errors = schemas.Gamecode().validate(payload)
    assert len(errors) > 0


def test_gamecode_schema_missing_data():
    payload = {}
    errors = schemas.Gamecode().validate(payload)
    assert len(errors) > 0


def test_gamecode_schema_success():
    gamecode = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4e'  # noqa: E501
    payload = {
        'gamecode': gamecode
    }
    errors = schemas.Gamecode().validate(payload)
    assert not errors


def test_unpaid_session_schema_wrong_datatype():
    gamecode = 1
    paid = 2
    payload = {
        'gamecode': gamecode,
        'paid': paid
    }
    errors = schemas.UnpaidSession().validate(payload)
    assert len(errors) > 0


def test_unpaid_session_schema_paid_true():
    gamecode = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4d'  # noqa: E501
    paid = True
    payload = {
        'gamecode': gamecode,
        'paid': paid
    }
    errors = schemas.UnpaidSession().validate(payload)
    assert len(errors) > 0


def test_unpaid_session_schema_missing_data():
    payload = {}
    errors = schemas.UnpaidSession().validate(payload)
    assert len(errors) > 0


def test_unpaid_session_schema_success():
    paid = False
    payload = {
        'paid': paid
    }
    errors = schemas.UnpaidSession().validate(payload)
    assert not errors


def test_signature_schema_wrong_datatype():
    v = '0x27'
    r = 79894344306498838818072926258834431728401637404261748372367030500850741067724  # noqa: E501
    s = 21802106681875645241820923929695615200446872719086150219705196063751203186893  # noqa: E501
    payload = {'v': v, 'r': r, 's': s}
    errors = schemas.Signature().validate(payload)
    assert len(errors) > 0


def test_signature_schema_hex_not_32_bytes():
    v = 27
    r = '0x2d3ce8d3b4978bb56e9411453b890d8fe8046c3face40ba1074a2e6a35'
    s = '0x29f3fc97295e0128173f694fbc8b75f3d0b3759dd58409727bb8d7e1c3'
    payload = {'v': v, 'r': r, 's': s}
    errors = schemas.Signature().validate(payload)
    assert len(errors) > 0


def test_signature_v_greater_than_max():
    v = 29
    r = '0x2d3ce8d3b4978bb56e9411453b890d8fe8046c3face40ba1074a2e6a357c9f9b'
    s = '0x29f3fc97295e0128173f694fbc8b75f3d0b3759dd58409727bb8d7e1c39f4c47'
    payload = {'v': v, 'r': r, 's': s}
    errors = schemas.Signature().validate(payload)
    assert len(errors) > 0


def test_signature_v_negative():
    v = -29
    r = '0x2d3ce8d3b4978bb56e9411453b890d8fe8046c3face40ba1074a2e6a357c9f9b'
    s = '0x29f3fc97295e0128173f694fbc8b75f3d0b3759dd58409727bb8d7e1c39f4c47'
    payload = {'v': v, 'r': r, 's': s}
    errors = schemas.Signature().validate(payload)
    assert len(errors) > 0


def test_signature_schema_missing_data():
    payload = {}
    errors = schemas.Signature().validate(payload)
    assert len(errors) > 0


def test_signature_schema_success():
    v = 28
    r = '0x2d3ce8d3b4978bb56e9411453b890d8fe8046c3face40ba1074a2e6a357c9f9b'
    s = '0x29f3fc97295e0128173f694fbc8b75f3d0b3759dd58409727bb8d7e1c39f4c47'
    payload = {'v': v, 'r': r, 's': s}
    errors = schemas.Signature().validate(payload)
    assert not errors


def test_auth_response_wrong_datatype():
    payload = {
        'gamecode': 1,
        'signature': {
            'v': 'A',
            'r': 'B',
            's': 'C',
        },
    }
    errors = schemas.AuthenticationResponse().validate(payload)
    assert len(errors) > 0


def test_auth_response_missing_data():
    payload = {}
    errors = schemas.AuthenticationResponse().validate(payload)
    assert len(errors) > 0


def test_auth_response_success():
    v = 28
    r = '0x2d3ce8d3b4978bb56e9411453b890d8fe8046c3face40ba1074a2e6a357c9f9b'
    s = '0x29f3fc97295e0128173f694fbc8b75f3d0b3759dd58409727bb8d7e1c39f4c47'
    gamecode = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4e'  # noqa: E501
    payload = {
        'gamecode': gamecode,
        'signature': {
            'v': v,
            'r': r,
            's': s,
        },
    }
    errors = schemas.AuthenticationResponse().validate(payload)
    assert not errors


def test_gamestate_schema_wrong_datatype():
    payload = {
        'board': 1,
        'gameover': 2,
        'score': 'A',
    }
    errors = schemas.Gamestate().validate(payload)
    assert len(errors) > 0


def test_gamestate_schema_missing_data():
    payload = {}
    errors = schemas.Gamestate().validate(payload)
    assert len(errors) > 0


def test_gamestate_schema_success():
    payload = {
        'board': [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        'gameover': False,
        'score': 0,
    }
    errors = schemas.Gamestate().validate(payload)
    assert not errors


def test_paid_session_schema_wrong_datatype():
    paid = 1
    gamestate = 2
    address = 3
    payload = {
        'paid': paid,
        'gamestate': gamestate,
        'address': address,
    }
    errors = schemas.PaidSession().validate(payload)
    assert len(errors) > 0


def test_paid_session_schema_paid_false(user):
    gamestate = {
        'board': [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        'gameover': False,
        'score': 0,
    }
    paid = False
    payload = {
        'gamestate': gamestate,
        'paid': paid,
        'address': user.address,
    }
    errors = schemas.PaidSession().validate(payload)
    assert len(errors) > 0


def test_paid_session_schema_missing_data():
    payload = {}
    errors = schemas.PaidSession().validate(payload)
    assert len(errors) > 0


def test_paid_session_schema_success(user):
    gamestate = {
        'board': [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        'gameover': False,
        'score': 0,
    }
    paid = True
    payload = {
        'gamestate': gamestate,
        'paid': paid,
        'address': user.address,
    }
    errors = schemas.PaidSession().validate(payload)
    assert not errors


def test_signed_gamestate_wrong_datatype():
    gamestate = 1
    gamecode = 2
    v = 'A'
    r = 'B'
    s = 'C'
    payload = {
        'gamestate': gamestate,
        'gamecode': gamecode,
        'signature': {
            'v': v,
            'r': r,
            's': s,
        }
    }
    errors = schemas.SignedGamestate().validate(payload)
    assert len(errors) > 0


def test_signed_gamestate_schema_missing_data():
    payload = {}
    errors = schemas.SignedGamestate().validate(payload)
    assert len(errors) > 0


def test_signed_gamestate_schema_success(user):
    gamestate = {
        'board': [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        'gameover': False,
        'score': 0,
    }
    gamecode = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4d'  # noqa: E501
    v = 28
    r = '0x2d3ce8d3b4978bb56e9411453b890d8fe8046c3face40ba1074a2e6a357c9f9b'
    s = '0x29f3fc97295e0128173f694fbc8b75f3d0b3759dd58409727bb8d7e1c39f4c47'
    payload = {
        'gamestate': gamestate,
        'gamecode': gamecode,
        'signature': {
            'v': v,
            'r': r,
            's': s,
        }
    }
    errors = schemas.SignedGamestate().validate(payload)
    assert not errors


def test_move_wrong_datatype():
    direction = 'A'
    gamecode = 1
    payload = {
        'gamecode': gamecode,
        'direction': direction,
    }
    errors = schemas.Move().validate(payload)
    assert len(errors) > 0


def test_move_missing_data():
    payload = {}
    errors = schemas.Move().validate(payload)
    assert len(errors) > 0


def test_move_direction_not_allowed():
    direction = 5
    gamecode = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4d'  # noqa: E501
    payload = {
        'gamecode': gamecode,
        'direction': direction,
    }
    errors = schemas.Move().validate(payload)
    assert len(errors) > 0


def test_move_success():
    direction = 1
    gamecode = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4d'  # noqa: E501
    payload = {
        'gamecode': gamecode,
        'direction': direction,
    }
    errors = schemas.Move().validate(payload)
    assert not errors
