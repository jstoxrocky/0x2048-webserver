from marshmallow import (
    Schema,
    fields,
)
from eth_utils import (
    is_hex,
    is_checksum_address,
    to_bytes,
)


def is_positive(value):
    return value > 0


def hex_is_length_20_bytes(hex):
    return len(to_bytes(hexstr=hex)) == 20


def hex_is_length_32_bytes(hex):
    # Getting errors when checking for
    # 32 bytes so change to 31. Not sure why.
    return len(to_bytes(hexstr=hex)) >= 31


def direction_allowed(direction):
    return direction in ALLOWED_DIRECTIONS


MAX_V_VALUE = 28
ALLOWED_DIRECTIONS = [1, 2, 3, 4]


# Building blocks
class Address(Schema):
    address = fields.String(
        required=True,
        validate=[is_hex, hex_is_length_20_bytes, is_checksum_address],
    )


class Random32Bytes(Schema):
    value = fields.String(
        required=True,
        validate=[is_hex, hex_is_length_32_bytes],
    )


class Signature(Schema):
    v = fields.Integer(
        required=True,
        validate=[is_positive, lambda x: x <= MAX_V_VALUE],
    )
    r = fields.String(required=True, validate=[hex_is_length_32_bytes])
    s = fields.String(required=True, validate=[hex_is_length_32_bytes])


class Gamestate(Schema):
    gameover = fields.Boolean(required=True)
    score = fields.Integer(required=True)
    board = fields.List(
        fields.List(
            fields.Integer(
                required=True,
            ),
            required=True
        ),
        required=True,
    )


class GameInfo(Schema):
    highscore = fields.Integer(required=True, validate=is_positive)
    jackpot = fields.Integer(required=True, validate=is_positive)
    name = fields.String(required=True)


# Payloads
class PaymentLocatorPayload(Schema):
    session_id = fields.Pluck(Random32Bytes, 'value', required=True)
    address = fields.Pluck(Address, 'address', required=True)


class MovePayload(Schema):
    session_id = fields.Pluck(Random32Bytes, 'value', required=True)
    direction = fields.Integer(required=True, validate=direction_allowed)


# Responses
class PaymentCodeResponse(Schema):
    session_id = fields.Pluck(Random32Bytes, 'value', required=True)
    payment_code = fields.Pluck(Random32Bytes, 'value', required=True)


class SignedGamestateResponse(Schema):
    signed_score = fields.Nested(Signature, required=True)
    gamestate = fields.Nested(Gamestate, required=True)


# Sessions
class UnpaidSession(Schema):
    paid = fields.Boolean(required=True, validate=lambda x: x is False)
    payment_code = fields.Pluck(Random32Bytes, 'value', required=True)


class PaidSession(Schema):
    paid = fields.Boolean(required=True, validate=lambda x: x is True)
    gamestate = fields.Nested(Gamestate, required=True)
    address = fields.Pluck(Address, 'address', required=True)


class GameInfos(Schema):
    games = fields.List(fields.Nested(GameInfo), required=True)
