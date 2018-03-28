from marshmallow import (
    Schema,
    fields,
)
from eth_utils import (
    is_hex,
    is_checksum_address,
)


MAX_V_VALUE = 28


class NonceSchema(Schema):
    """
    Validate emitted nonce data structures
    """
    nonce = fields.Str(required=True, validate=is_hex)


class MoveSchema(Schema):
    """
    Validate recieved move data structures
    """
    user = fields.Str(required=True, validate=is_checksum_address)
    direction = fields.Integer(required=True)


class SimpleSignatureSchema(Schema):
    signature = fields.Str(required=True, validate=is_hex)


class FullSignatureSchema(Schema):
    message = fields.Str(required=True, validate=is_hex)
    messageHash = fields.Str(required=True, validate=is_hex)
    v = fields.Integer(required=True, validate=lambda x: x <= MAX_V_VALUE)
    r = fields.Str(required=True, validate=is_hex)
    s = fields.Str(required=True, validate=is_hex)
    signature = fields.Str(SimpleSignatureSchema, required=True)


class GamestateSchema(Schema):
    """
    Validate emitted gamestate data structures
    """
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


class SignedGamestateSchema(GamestateSchema):
    """
    Validate emitted signed gamestate data structures
    """
    signature = fields.Nested(FullSignatureSchema, required=True)
