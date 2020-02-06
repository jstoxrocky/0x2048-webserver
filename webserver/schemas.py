from marshmallow import (
    Schema,
    fields,
)
from eth_utils import (
    is_hex,
    is_checksum_address,
)


MAX_V_VALUE = 28


class Nonce(Schema):
    """
    Validate emitted nonce data structures
    """
    nonce = fields.String(required=True, validate=is_hex)


class Move(Schema):
    """
    Validate recieved move data structures
    """
    direction = fields.Integer(required=True)


class SimpleSignature(Schema):
    signature = fields.String(required=True, validate=is_hex)


class Receipt(Schema):
    # Pluck runs the child validations (is_hex)
    signature = fields.Pluck(SimpleSignature, 'signature', required=True)
    txhash = fields.String(required=True, validate=is_hex)


class FullSignature(Schema):
    messageHash = fields.String(required=True, validate=is_hex)
    v = fields.Integer(required=True, validate=lambda x: x <= MAX_V_VALUE)
    r = fields.Integer(required=True)
    s = fields.Integer(required=True)
    signature = fields.Pluck(SimpleSignature, 'signature', required=True)


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


class SignedGamestate(Gamestate):
    signature = fields.Nested(FullSignature, required=True)
    recoveredAddress = fields.String(
        required=True,
        validate=is_checksum_address,
    )
