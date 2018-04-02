from flask import (
    jsonify,
    Blueprint,
    session,
    request,
)
from flask_cors import (
    cross_origin,
)
from webserver.config import (
    ORIGINS,
    PRIV,
    ARCADE_ADDRESS,
)
from webserver import exceptions
from webserver import (
    state_channel,
)
from webserver.contract import (
    contract,
    wait_for_transaction_receipt,
)
from webserver import schemas
from webserver.gameplay import (
    new,
)
from toolz.dicttoolz import (
    merge,
)
from eth_utils import (
    decode_hex,
)


blueprint = Blueprint('payment', __name__)


@blueprint.route('/nonce', methods=['GET'])
@cross_origin(origins=ORIGINS, methods=['GET'],
              supports_credentials=True)
def generate_nonce_challenge():
    """
    Generate a nonce for a user to sign
    Associate the nonce with the session
    """
    # Reset values upon request for new nonce
    session['paid'] = False
    session['nonce'] = None
    # Get random value for nonce
    # Associate the nonce with this session
    nonce = state_channel.generate_random_nonce()
    session['nonce'] = nonce
    return jsonify({'nonce': nonce})


@blueprint.route('/payment-confirmation', methods=['GET'])
@cross_origin(origins=ORIGINS, methods=['GET'],
              supports_credentials=True)
def confirm_payment():
    """
    Recover the signer from the signed nonce
    and verify that the signer has paid by checking the Arcade contract nonce
    """
    # Cannot have already paid
    if session.get('paid', False):
        raise exceptions.UnexpectedPaymentAttempt
    # Must have nonce
    if not session.get('nonce', None):
        raise exceptions.UnexpectedEmptyNonce
    # Validate payload
    payload = request.args
    print(payload)
    if schemas.Receipt().validate(payload):
        raise exceptions.ValidationError
    # Whoever signs the nonce is our user-address
    messageHash = state_channel.prepare_messageHash_for_signing(
        session['nonce'],
    )
    signer = state_channel.recover(messageHash, payload['signature'])
    # Wait for transaction to be mined
    wait_for_transaction_receipt(txn_hash=payload['txhash'], timeout=120)
    # Check contract nonce
    nonce = contract.functions.getNonce(signer).call()
    if nonce != decode_hex(session['nonce']):
        raise exceptions.UnexpectedContractNonce
    # Start a new game
    session['paid'] = True
    new_state = new()
    msg = state_channel.solidity_keccak(
        ARCADE_ADDRESS,
        session['address'],
        new_state['score'],
    )
    signature = state_channel.sign(msg, PRIV)
    session['state'] = merge(new_state, {'signature': signature})
    return jsonify(session['state'])
