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
from webserver.config import (
    ARCADE_ADDRESS,
    PRIV,
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


def sign_score(user, score):
    structured_highscore = STRUCTURED_HIGHSCORE
    structured_highscore["message"] = {
        "user": user,
        "score": score,
    }
    structured_highscore["domain"]["verifyingContract"] = ARCADE_ADDRESS
    structured_msg = encode_structured_data(
        primitive=structured_highscore,
    )
    signature = Account.sign_message(structured_msg, PRIV)
    signature = valmap(
        lambda x: x.hex() if isinstance(x, bytes) else x,
        signature,
    )
    signature['r'] = HexBytes(signature['r']).hex()
    signature['s'] = HexBytes(signature['s']).hex()
    return signature


def random_32bytes():
    value = HexBytes(os.urandom(32))
    return value.hex()
