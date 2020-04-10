from webserver import (
    schemas,
)
from webserver.game_config import (
    TWENTY_FORTY_EIGHT,
)


def test_game_info_schema_wrong_datatype():
    payload = {
        'id': 1,
        'highscore': 'A',
        'jackpot': 'B',
        'name': 1,
    }
    errors = schemas.GameInfo().validate(payload)
    assert len(errors) > 0


def test_game_info_schema_missing_data():
    payload = {}
    errors = schemas.GameInfo().validate(payload)
    assert len(errors) > 0


def test_game_info_schema_negative():
    payload = {
        'id': TWENTY_FORTY_EIGHT,
        'highscore': -1,
        'jackpot': -2,
        'name': 'Cool game',
    }
    errors = schemas.GameInfo().validate(payload)
    assert len(errors) > 0


def test_game_info_schema_success():
    payload = {
        'id': TWENTY_FORTY_EIGHT,
        'highscore': 1,
        'jackpot': 2,
        'name': 'Cool game'
    }
    errors = schemas.GameInfo().validate(payload)
    assert not errors


def test_game_info_id_not_real():
    payload = {
        'id': '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4d',  # noqa: E501
        'highscore': 1,
        'jackpot': 2,
        'name': 'Cool game'
    }
    errors = schemas.GameInfo().validate(payload)
    assert len(errors) > 0


def test_game_infos_schema_success():
    payload = {
        'games': [{
            'id': TWENTY_FORTY_EIGHT,
            'highscore': 1,
            'jackpot': 2,
            'name': 'Cool game'
        }],
    }
    errors = schemas.GameInfos().validate(payload)
    assert not errors


def test_random32bytes_schema_wrong_datatype():
    payload = {'value': 1}
    errors = schemas.Random32Bytes().validate(payload)
    assert len(errors) > 0


def test_random32bytes_schema_missing_data():
    payload = {}
    errors = schemas.Random32Bytes().validate(payload)
    assert len(errors) > 0


def test_random32bytes_schema_hex_not_32_bytes():
    value = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47'
    payload = {
        'value': value,
    }
    errors = schemas.Random32Bytes().validate(payload)
    assert len(errors) > 0


def test_random32bytes_schema_success():
    value = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4d'  # noqa: E501
    payload = {
        'value': value,
    }
    errors = schemas.Random32Bytes().validate(payload)
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


def test_payment_code_schema_wrong_datatype():
    payment_code = 1
    session_id = 2
    payload = {
        'payment_code': payment_code,
        'session_id': session_id
    }
    errors = schemas.PaymentCodeResponse().validate(payload)
    assert len(errors) > 0


def test_payment_code_schema_missing_data():
    payload = {}
    errors = schemas.PaymentCodeResponse().validate(payload)
    assert len(errors) > 0


def test_payment_code_schema_success():
    payment_code = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4d'  # noqa: E501
    session_id = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4e'  # noqa: E501
    payload = {
        'payment_code': payment_code,
        'session_id': session_id
    }
    errors = schemas.PaymentCodeResponse().validate(payload)
    assert not errors


def test_unpaid_session_schema_wrong_datatype():
    payment_code = 1
    paid = 2
    payload = {
        'payment_code': payment_code,
        'paid': paid
    }
    errors = schemas.UnpaidSession().validate(payload)
    assert len(errors) > 0


def test_unpaid_session_schema_paid_true():
    payment_code = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4d'  # noqa: E501
    paid = True
    payload = {
        'payment_code': payment_code,
        'paid': paid
    }
    errors = schemas.UnpaidSession().validate(payload)
    assert len(errors) > 0


def test_unpaid_session_schema_missing_data():
    payload = {}
    errors = schemas.UnpaidSession().validate(payload)
    assert len(errors) > 0


def test_unpaid_session_schema_success():
    payment_code = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4d'  # noqa: E501
    paid = False
    payload = {
        'payment_code': payment_code,
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


def test_payment_locator_payload_wrong_datatype():
    payload = {
        'session_id': 1,
        'address': 1,
        'game_id': 1,
    }
    errors = schemas.PaymentLocatorPayload().validate(payload)
    assert len(errors) > 0


def test_payment_locator_payload_missing_data():
    payload = {}
    errors = schemas.PaymentLocatorPayload().validate(payload)
    assert len(errors) > 0


def test_payment_locator_payload_game_id_not_real():
    session_id = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4e'  # noqa: E501
    address = '0xc519A51c6cC9B36e6cEbcC732b9036dAffc69B5B'
    game_id = '0x34a8bcaf7e336f18e5f5eeca59336015b6cdfa5c66f1364a19b7c539971cfbcf'  # noqa: E501
    payload = {
        'session_id': session_id,
        'address': address,
        'game_id': game_id,
    }
    errors = schemas.PaymentLocatorPayload().validate(payload)
    assert len(errors) > 0


def test_payment_locator_payload_success():
    session_id = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4e'  # noqa: E501
    address = '0xc519A51c6cC9B36e6cEbcC732b9036dAffc69B5B'
    game_id = TWENTY_FORTY_EIGHT
    payload = {
        'session_id': session_id,
        'address': address,
        'game_id': game_id,
    }
    errors = schemas.PaymentLocatorPayload().validate(payload)
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
    game_id = 4
    payload = {
        'paid': paid,
        'gamestate': gamestate,
        'address': address,
        'game_id': game_id,
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
    game_id = TWENTY_FORTY_EIGHT  # noqa: E501
    payload = {
        'gamestate': gamestate,
        'paid': paid,
        'address': user.address,
        'game_id': game_id,
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
    game_id = TWENTY_FORTY_EIGHT
    payload = {
        'gamestate': gamestate,
        'paid': paid,
        'address': user.address,
        'game_id': game_id,
    }
    errors = schemas.PaidSession().validate(payload)
    assert not errors


def test_paid_session_game_id_not_real(user):
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
    game_id = '0x34a8bcaf7e336f18e5f5eeca59336015b6cdfa5c66f1364a19b7c539971cfbcf'  # noqa: 501
    payload = {
        'gamestate': gamestate,
        'paid': paid,
        'address': user.address,
        'game_id': game_id,
    }
    errors = schemas.PaidSession().validate(payload)
    assert len(errors) > 0


def test_signed_gamestate_wrong_datatype():
    gamestate = 1
    v = 'A'
    r = 'B'
    s = 'C'
    payload = {
        'gamestate': gamestate,
        'signed_score': {
            'v': v,
            'r': r,
            's': s,
        }
    }
    errors = schemas.SignedGamestateResponse().validate(payload)
    assert len(errors) > 0


def test_signed_gamestate_schema_missing_data():
    payload = {}
    errors = schemas.SignedGamestateResponse().validate(payload)
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
    v = 28
    r = '0x2d3ce8d3b4978bb56e9411453b890d8fe8046c3face40ba1074a2e6a357c9f9b'
    s = '0x29f3fc97295e0128173f694fbc8b75f3d0b3759dd58409727bb8d7e1c39f4c47'
    payload = {
        'gamestate': gamestate,
        'signed_score': {
            'v': v,
            'r': r,
            's': s,
        }
    }
    errors = schemas.SignedGamestateResponse().validate(payload)
    assert not errors


def test_move_payload_wrong_datatype():
    direction = 'A'
    session_id = 1
    payload = {
        'direction': direction,
        'session_id': session_id,
    }
    errors = schemas.MovePayload().validate(payload)
    assert len(errors) > 0


def test_move_payload_missing_data():
    payload = {}
    errors = schemas.MovePayload().validate(payload)
    assert len(errors) > 0


def test_move_payload_direction_not_allowed():
    direction = 5
    session_id = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4e'  # noqa: E501
    payload = {
        'direction': direction,
        'session_id': session_id,
    }
    errors = schemas.MovePayload().validate(payload)
    assert len(errors) > 0


def test_move_payload_success():
    direction = 1
    session_id = '0x4a3c9000acbe7d73d0d6dcea6abd664006dadbd4d7c37c7095635c9c47ca1d4e'  # noqa: E501
    payload = {
        'direction': direction,
        'session_id': session_id,
    }
    errors = schemas.MovePayload().validate(payload)
    assert not errors
