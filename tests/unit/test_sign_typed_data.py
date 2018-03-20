from eth_utils import (
    encode_hex,
    to_bytes,
)
from eth_keys import (
    keys,
)
from eth_account.signing import (
    to_eth_v,
    to_bytes32,
)
from webserver.state_channel import (
    hash_typed_data,
    raw_sign,
)


def test_one_string_match_metamask(user):
    expected_signature = "0x37046cbd93c61d05780990b217803a9f2659ac0742f8af26bdd714054e9206825c0dbd25a8eb795334dd616870509c26daf235f8d5511761038841fc01707bb91b"  # noqa: E501
    msg_params = [
        {'type': 'string', 'name': 'x', 'value': 'x'},
    ]
    msg_hash = hash_typed_data(msg_params)
    raw_signature = raw_sign(msg_hash, user.privateKey)
    v_raw, r, s = raw_signature.vrs
    v = to_eth_v(v_raw)
    signature = encode_hex(to_bytes32(r) + to_bytes32(s) + to_bytes(v))
    assert signature == expected_signature


def test_one_number_match_metamask(user):
    expected_signature = "0x4b7b7cfe2007fc1556c8ed62a38a5fe726b5a62d82ed05c7a5624745e7398ddd3eeed7694502c397c108ab9e9f3971fae9dc4c11952e8fd154324351c0a859eb1b"  # noqa: E501
    msg_params = [
        {'type': 'uint256', 'name': 'x', 'value': 1},
    ]
    msg_hash = hash_typed_data(msg_params)
    key = keys.PrivateKey(user.privateKey)
    raw_signature = key.sign_msg_hash(msg_hash)
    v_raw, r, s = raw_signature.vrs
    v = to_eth_v(v_raw)
    signature = encode_hex(to_bytes32(r) + to_bytes32(s) + to_bytes(v))
    assert signature == expected_signature


def test_two_strings_match_metamask(user):
    expected_signature = "0x1c4231c575073ae397a6942b71352ce9aa39f8926a234df90ad141848be2ad6f19a404dde925b31e079d2f235f8ed5030b60f3a70002460d7e35984f177da64c1c"  # noqa: E501
    msg_params = [
        {'type': 'string', 'name': 'x', 'value': 'x'},
        {'type': 'string', 'name': 'y', 'value': 'y'},
    ]
    msg_hash = hash_typed_data(msg_params)
    key = keys.PrivateKey(user.privateKey)
    raw_signature = key.sign_msg_hash(msg_hash)
    v_raw, r, s = raw_signature.vrs
    v = to_eth_v(v_raw)
    signature = encode_hex(to_bytes32(r) + to_bytes32(s) + to_bytes(v))
    assert signature == expected_signature


def test_one_string_one_number_match_metamask(user):
    expected_signature = "0x4cbac857f704548e5657290b4b31b9a7ad0d20844b43561bc0d548b71a62d8c11ead220a70e01fee7132bd247260fc7ece61bbfb20306bae60e5eb3f9c0d56591c"  # noqa: E501
    msg_params = [
        {'type': 'string', 'name': 'x', 'value': 'x'},
        {'type': 'uint256', 'name': 'y', 'value': 1},
    ]
    msg_hash = hash_typed_data(msg_params)
    key = keys.PrivateKey(user.privateKey)
    raw_signature = key.sign_msg_hash(msg_hash)
    v_raw, r, s = raw_signature.vrs
    v = to_eth_v(v_raw)
    signature = encode_hex(to_bytes32(r) + to_bytes32(s) + to_bytes(v))
    assert signature == expected_signature


def test_eip_example(user):
    expected_signature = "0xf9e588003f10c8eaf7c5cc178001f3378c8e55e9218b580ff876266f72a8a11454654f800741a87c1347bc40380ed77bd13206781598a1b296d9d72d73d29d231c"  # noqa: E501
    msg_params = [
        {'type': 'string', 'name': 'Message', 'value': 'Hi, Alice!'},
        {'type': 'uint32', 'name': 'A number', 'value': 1337},
    ]
    msg_hash = hash_typed_data(msg_params)
    key = keys.PrivateKey(user.privateKey)
    raw_signature = key.sign_msg_hash(msg_hash)
    v_raw, r, s = raw_signature.vrs
    v = to_eth_v(v_raw)
    signature = encode_hex(to_bytes32(r) + to_bytes32(s) + to_bytes(v))
    assert signature == expected_signature
