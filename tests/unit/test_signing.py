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
from webserver.game_config import (
    TWENTY_FORTY_EIGHT as GAME_ID,
)
from eth_abi.packed import (
    encode_abi_packed,
)


def test_sign_score(user, owner, monkeypatch):
    monkeypatch.setattr("webserver.signing.PRIV", owner.key)
    expected_signer = owner.address

    score = 1
    vrs = sign_score(GAME_ID, user.address, score)
    types = ['bytes32', 'address', 'uint256']
    values = [
        HexBytes(GAME_ID),
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
