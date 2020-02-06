from webserver.signing import (
    sign_score,
    recover_signer_from_signed_nonce,
    generate_random_nonce,
    STRUCTURED_HIGHSCORE,
    STRUCTURED_NONCE,
)
from webserver.config import (
    ARCADE_ADDRESS,
)
from web3 import (
    Account,
)
from eth_account.messages import (
    encode_structured_data,
)


def test_sign_score(user, owner):
    score = 1
    structured_highscore = STRUCTURED_HIGHSCORE
    structured_highscore["message"] = {
        "user": user.address,
        "score": score,
    }
    structured_highscore["domain"]["verifyingContract"] = ARCADE_ADDRESS
    structured_msg = encode_structured_data(
        primitive=structured_highscore,
    )
    expected_signer = Account.from_key(owner.key).address
    signature = sign_score(owner.key, ARCADE_ADDRESS, user.address, score)
    actual_signer = Account.recover_message(
        structured_msg,
        signature=signature['signature'],
    )
    assert actual_signer == expected_signer


def test_recover_signer_from_signed_nonce(user):
    nonce = b'\x01' * 32
    structured_nonce = STRUCTURED_NONCE
    structured_nonce["message"] = {
        "nonce": nonce,
    }
    structured_nonce["domain"]["verifyingContract"] = ARCADE_ADDRESS
    structured_msg = encode_structured_data(
        primitive=structured_nonce,
    )
    expected_signer = user.address
    signature = Account.sign_message(structured_msg, user.key)
    # This hardcoded assertion is necessary.
    # Metamask has changed the way EIP 712 is implemented at least
    # four times so far (as of Feb. 2020). In the Arcade game, the user
    # will sign the nonce in the browser via Metamask. We then recover the
    # signer's address from the signature on the server side via the Python
    # implementation. For this reason, we need to ensure that Metamask is
    # hashing and signing according to EIP 712 in the same way that the Python
    # implementation is. This hardcoded value matches what Metamask would give
    # for the same StructuredData (bytes32 is a 0x prefixed hex string
    # for Metamask).
    assert signature['signature'].hex() == '0x912892885067b2aac5eafd080d8438d6235c369e626d8d64efcee56ef58c141077f0e72b77a853b6a3a5a7bfaa439a17603a0b375cb8caac7e2e81d55be924f11c'  # noqa: E501
    actual_signer = recover_signer_from_signed_nonce(
        ARCADE_ADDRESS,
        nonce,
        signature['signature'],
    )
    assert actual_signer == expected_signer


def test_generate_random_nonce():
    nonce = generate_random_nonce()
    assert len(nonce) == 32
