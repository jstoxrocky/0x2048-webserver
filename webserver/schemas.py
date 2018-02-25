from marshmallow import (
    Schema,
    fields,
)
from eth_utils import (
    is_hex,
    is_checksum_address,
)


MAX_V_VALUE = 28


class UserSchema(Schema):
    user = fields.Str(required=True, validate=is_checksum_address)


class SignatureSchema(Schema):
    message = fields.Str(required=True, validate=is_hex)
    messageHash = fields.Str(required=True, validate=is_hex)
    v = fields.Integer(required=True, validate=lambda _v: _v <= MAX_V_VALUE)
    r = fields.Str(required=True, validate=is_hex)
    s = fields.Str(required=True, validate=is_hex)
    signature = fields.Str(required=True, validate=is_hex)


class GamestateSchema(Schema):
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
    gameover = fields.Boolean(required=True)
    signature = fields.Nested(SignatureSchema, required=True)


class IOUSchema(Schema):
    value = fields.Integer(required=True)
    signature = fields.Nested(SignatureSchema, required=True)
    user = fields.Str(UserSchema, required=True)


class MoveSchema(Schema):
    user = fields.Str(required=True, validate=is_checksum_address)
    direction = fields.Integer(required=True)
