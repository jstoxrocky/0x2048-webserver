from flask import (
    jsonify,
    request,
    Blueprint
)
from flask_cors import (
    cross_origin,
)
from webserver.exceptions import (
    MissingUser,
)
from webserver import (
    state_channel,
)
from webserver.price import (
    get_current_dollar_price_in_wei,
)
from webserver.config import (
    ORIGINS,
)
from eth_utils import (
    is_checksum_address,
)
from toolz.dicttoolz import (
    merge,
)
from webserver.config import (
    PRIV,
    ADDR,
)

blueprint = Blueprint('price', __name__)


@blueprint.route('/price', methods=['GET'])
@cross_origin(origins=ORIGINS, methods=['GET'], supports_credentials=True)
def price():
    # State-channel signature requires a user's address
    user = request.args.get('user')
    if not is_checksum_address(user):
        raise MissingUser
    # Get price
    price = get_current_dollar_price_in_wei()
    # Create state-channel specific signature
    signature = state_channel.sign(PRIV, ADDR, user, price)
    return jsonify(merge({'signature': signature}, {'price': price}))
