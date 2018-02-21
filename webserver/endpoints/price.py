from flask import (
    jsonify,
    request,
    Blueprint
)
from flask_cors import (
    cross_origin,
)
from webserver.exceptions import (
    ValidationError,
)
from webserver import (
    state_channel,
)
from webserver.price import (
    get_price,
    to_wei_per_dollar,
)
from webserver.config import (
    ORIGINS,
)
from toolz.dicttoolz import (
    merge,
)
from webserver.config import (
    PRIV,
    ARCADE_ADDR,
)
from webserver.schemas import (
    PriceSchema,
)

blueprint = Blueprint('price', __name__)


@blueprint.route('/price', methods=['GET'])
@cross_origin(origins=ORIGINS, methods=['GET'], supports_credentials=True)
def price():
    # Validate payload
    payload = request.args
    if PriceSchema().validate(payload):
        raise ValidationError
    # Get price
    price_in_dollars = get_price()
    price = to_wei_per_dollar(price_in_dollars)
    # Create state-channel specific signature
    msg = state_channel.solidity_keccak(ARCADE_ADDR, payload['user'], price)
    signature = state_channel.sign(msg, PRIV)
    return jsonify(merge({'signature': signature}, {'price': price}))
