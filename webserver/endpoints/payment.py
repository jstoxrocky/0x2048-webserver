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
    signing,
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
    nonce = signing.generate_random_nonce().hex()
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
    if schemas.Receipt().validate(payload):
        raise exceptions.ValidationError
    # Whoever signs the nonce is our user-address
    recoveredAddress = signing.recover_signer_from_signed_nonce(
        ARCADE_ADDRESS,
        session['nonce'],
        payload['signature'],
    )
    session['recoveredAddress'] = recoveredAddress
    # Wait for transaction to be mined
    wait_for_transaction_receipt(txn_hash=payload['txhash'], timeout=120)
    # Check contract nonce
    nonce = contract.functions.getNonce(session['recoveredAddress']).call()
    if nonce != session['nonce']:
        raise exceptions.UnexpectedContractNonce
    # Start a new game
    session['paid'] = True
    state = new()
    # For information on why these three variables are included in the
    # hash, check the contract source code in the contract repositiory.
    signed_score = signing.sign_score(
        PRIV,
        ARCADE_ADDRESS,
        session['recoveredAddress'],
        state['score']
    )
    session['state'] = merge(
        state, {
            'signature': signed_score,
            'recoveredAddress': session['recoveredAddress'],
        }
    )
    return jsonify(session['state'])
