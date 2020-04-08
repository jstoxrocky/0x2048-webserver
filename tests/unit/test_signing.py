from webserver.signing import (
    sign_score,
    random_32bytes,
    STRUCTURED_HIGHSCORE,
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
from hexbytes import (
    HexBytes,
)


def test_sign_score(user, owner, monkeypatch):
    monkeypatch.setattr("webserver.signing.PRIV", owner.key)
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
    signature = sign_score(user.address, score)
    actual_signer = Account.recover_message(
        structured_msg,
        signature=signature['signature'],
    )
    assert actual_signer == expected_signer


def test_generate_random_32bytes():
    value = HexBytes(random_32bytes())
    assert len(value) == 32
