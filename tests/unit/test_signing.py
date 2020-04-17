from webserver.signing import (
    sign_score,
    random_32bytes,
)
from webserver.config import (
    ARCADE_ADDRESS,
)
from web3 import (
    Account,
)
from eth_account.messages import (
    encode_intended_validator,
)
from hexbytes import (
    HexBytes,
)
from game.game import (
    TwentyFortyEight,
)
from eth_abi.packed import (
    encode_abi_packed,
)


def test_sign_score(user, owner, monkeypatch):
    monkeypatch.setattr("webserver.signing.PRIV", owner.key)
    expected_signer = owner.address
    game = TwentyFortyEight

    score = 1
    vrs = sign_score(game.id, user.address, score)
    types = ['bytes32', 'address', 'uint256']
    values = [
        HexBytes(game.id),
        user.address,
        score,
    ]
    encoded_values = encode_abi_packed(types, values)
    message = encode_intended_validator(
        validator_address=ARCADE_ADDRESS,
        primitive=encoded_values,
    )
    actual_signer = Account.recover_message(
        message,
        vrs=vrs,
    )

    assert actual_signer == expected_signer


def test_generate_random_32bytes():
    value = HexBytes(random_32bytes())
    assert len(value) == 32
