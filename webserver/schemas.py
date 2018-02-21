from marshmallow import (
    Schema,
    fields,
)
from eth_utils import (
    is_hex,
    is_checksum_address,
)


MAX_V_VALUE = 28


class SignatureSchema(Schema):
    message = fields.Str(required=True, validate=is_hex)
    messageHash = fields.Str(required=True, validate=is_hex)
    v = fields.Integer(required=True, validate=lambda _v: _v <= MAX_V_VALUE)
    r = fields.Str(required=True, validate=is_hex)
    s = fields.Str(required=True, validate=is_hex)
    signature = fields.Str(required=True, validate=is_hex)
    user = fields.Str(required=True, validate=is_checksum_address)
    value = fields.Integer(required=True)


class MoveSchema(Schema):
    user = fields.Str(required=True, validate=is_checksum_address)
    direction = fields.Integer(required=True)


class PriceSchema(Schema):
    user = fields.Str(required=True, validate=is_checksum_address)
