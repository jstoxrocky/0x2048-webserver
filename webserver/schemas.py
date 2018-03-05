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
    """
    Validate user input when calling GET /iou route
    """
    user = fields.Str(required=True, validate=is_checksum_address)


class SimpleSignatureSchema(Schema):
    signature = fields.Str(required=True, validate=is_hex)


class FullSignatureSchema(Schema):
    message = fields.Str(required=True, validate=is_hex)
    messageHash = fields.Str(required=True, validate=is_hex)
    v = fields.Integer(required=True, validate=lambda _v: _v <= MAX_V_VALUE)
    r = fields.Str(required=True, validate=is_hex)
    s = fields.Str(required=True, validate=is_hex)
    signature = fields.Str(SimpleSignatureSchema, required=True)


class IOUSchema(Schema):
    """
    Validate user input when calling POST /iou route
    """
    value = fields.Integer(required=True)
    signature = fields.Str(SimpleSignatureSchema, required=True)
    user = fields.Str(UserSchema, required=True)


class MoveSchema(Schema):
    """
    Validate user input when calling POST /move route
    """
    user = fields.Str(required=True, validate=is_checksum_address)
    direction = fields.Integer(required=True)


class GamestateSchema(Schema):
    """
    Validate gameplay output
    """
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


class SignedGamestateSchema(Schema):
    """
    Validate server output when calling POST /move or GET /gamestate
    """
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
    signature = fields.Nested(FullSignatureSchema, required=True)
