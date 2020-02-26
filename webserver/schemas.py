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
    return len(to_bytes(hexstr=hex)) == 32


def direction_allowed(direction):
    return direction in ALLOWED_DIRECTIONS


MAX_V_VALUE = 28
ALLOWED_DIRECTIONS = [1, 2, 3, 4]


class Address(Schema):
    address = fields.String(
        required=True,
        validate=[is_hex, hex_is_length_20_bytes, is_checksum_address],
    )


class Nonce(Schema):
    nonce = fields.String(
        required=True,
        validate=[is_hex, hex_is_length_32_bytes],
    )


class Challenge(Schema):
    session_id = fields.Pluck(Nonce, 'nonce', required=True)
    challenge = fields.Pluck(Nonce, 'nonce', required=True)


class UnpaidSession(Schema):
    paid = fields.Boolean(required=True, validate=lambda x: x is False)
    challenge = fields.Pluck(Nonce, 'nonce', required=True)


class Signature(Schema):
    v = fields.Integer(
        required=True,
        validate=[is_positive, lambda x: x <= MAX_V_VALUE],
    )
    r = fields.String(required=True, validate=[hex_is_length_32_bytes])
    s = fields.String(required=True, validate=[hex_is_length_32_bytes])


class ChallengeResponse(Schema):
    session_id = fields.Pluck(Nonce, 'nonce', required=True)
    signature = fields.Nested(Signature, required=True)


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


class PaidSession(Schema):
    paid = fields.Boolean(required=True, validate=lambda x: x is True)
    gamestate = fields.Nested(Gamestate, required=True)
    recovered_address = fields.Pluck(Address, 'address', required=True)


class SignedGamestate(Schema):
    session_id = fields.Pluck(Nonce, 'nonce', required=True)
    signature = fields.Nested(Signature, required=True)
    gamestate = fields.Nested(Gamestate, required=True)


class Move(Schema):
    session_id = fields.Pluck(Nonce, 'nonce', required=True)
    direction = fields.Integer(required=True, validate=direction_allowed)
