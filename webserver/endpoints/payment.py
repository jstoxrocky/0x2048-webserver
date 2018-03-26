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
)
from webserver import exceptions
from webserver import (
    state_channel,
)
from webserver.contract import (
    contract,
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
    # Cannot have already paid
    if session.get('paid', False):
        raise exceptions.UnexpectedPaymentAttempt
    # Must not have nonce
    if session.get('nonce', None):
        raise exceptions.UnexpectedNonceGenerationAttempt
    # Get random value for nonce
    # Associate the nonce with this session
    nonce = state_channel.generate_random_nonce()
    session['nonce'] = nonce
    return jsonify({'nonce': nonce})


@blueprint.route('/address-confirmation', methods=['GET'])
@cross_origin(origins=ORIGINS, methods=['GET'],
              supports_credentials=True)
def calculate_address():
    """
    Associate the signer with the session
    """
    # Cannot have already paid
    if session.get('paid', False):
        raise exceptions.UnexpectedPaymentAttempt
    # Must have nonce
    if not session.get('nonce', None):
        raise exceptions.UnexpectedEmptyNonce
    # Whoever signs this random nonce is our user-address
    signature = request.get_json()
    messageHash = state_channel.prepare_messageHash_for_signing(
        session['nonce'],
    )
    signer = state_channel.recover(messageHash, signature)
    session['address'] = signer
    return jsonify({'success': True})


@blueprint.route('/payment-confirmation', methods=['GET'])
@cross_origin(origins=ORIGINS, methods=['GET'],
              supports_credentials=True)
def confirm_payment():
    """
    Verify that the user has paid by checking the nonce value added to
    the contract
    """
    # Cannot have already paid
    if session.get('paid', False):
        raise exceptions.UnexpectedPaymentAttempt
    # Must have nonce
    if not session.get('nonce', None):
        raise exceptions.UnexpectedEmptyNonce

    nonce = contract.functions.getNonce(session['address']).call()
    if nonce != session['nonce']:
        raise exceptions.UnexpectedContractNonce

    session['paid'] = True
    return jsonify({'success': True})
