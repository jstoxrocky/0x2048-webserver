from web3 import (
    Account,
)
from eth_account.messages import (
    encode_structured_data,
)
from toolz.dicttoolz import (
    valmap,
)
from hexbytes import (
    HexBytes,
)
import os


STRUCTURED_HIGHSCORE = {
    "types": {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"}
        ],
        "Highscore": [
            {"name": "user", "type": "address"},
            {"name": "score", "type": "uint256"}
        ],
    },
    "primaryType": "Highscore",
    "domain": {
        "name": "0x2048",
        "version": "1.0",
        "chainId": 1,
    },
}


STRUCTURED_NONCE = {
    "types": {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"}
        ],
        "Nonce": [
            {"name": "nonce", "type": "bytes32"},
        ],
    },
    "primaryType": "Nonce",
    "domain": {
        "name": "0x2048",
        "version": "1.0",
        "chainId": 1,
    },
}


def sign_score(private_key, contract, user, score):
    structured_highscore = STRUCTURED_HIGHSCORE
    structured_highscore["message"] = {
        "user": user,
        "score": score,
    }
    structured_highscore["domain"]["verifyingContract"] = contract
    structured_msg = encode_structured_data(
        primitive=structured_highscore,
    )
    # sign_message passes data through
    # eth_account.messages._hash_eip191_message which is keccak256
    signature = Account.sign_message(structured_msg, private_key)
    signature = valmap(
        lambda x: x.hex() if isinstance(x, bytes) else x,
        signature,
    )
    return signature


def prepare_structured_nonce_for_signing(contract, nonce):
    # We are assuming that metamask with hash and sign
    # the nonce as bytes. If it instead signs it as a string, we need to know.
    # Whether we treat the nonce as bytes or string depends on metamask.
    structured_nonce = STRUCTURED_NONCE
    structured_nonce["message"] = {
        "nonce": nonce,
    }
    structured_nonce["domain"]["verifyingContract"] = contract
    structured_msg = encode_structured_data(
        primitive=structured_nonce,
    )
    return structured_msg


def recover_signer_from_signed_nonce(contract, nonce, signature):
    message = prepare_structured_nonce_for_signing(contract, nonce)
    signer = Account.recover_message(message, signature=signature)
    return signer


def generate_random_nonce():
    nonce = HexBytes(os.urandom(32))
    return nonce
