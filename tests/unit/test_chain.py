from webserver.chain import (
    calc_net_time_left,
    calc_net_balance,
)
from eth_utils import (
    to_wei,
)


def test_net_time_left_positive(mocker, user):
    """
    Net time left should be positive and equal to 60 * 60 * 24 * (3 - 1)
    """
    contract = mocker.patch('webserver.chain.contract')
    contract.functions.timeoutOf.return_value.call.return_value = 60 * 60 * 24 * 3  # noqa: E501
    net_time_left = calc_net_time_left(user.address)
    assert net_time_left == 60 * 60 * 24 * (3 - 1)


def test_net_time_left_negative(mocker, user):
    """
    Net time left should be negative and equal to 60 * 60 * (23 - 24)
    """
    contract = mocker.patch('webserver.chain.contract')
    contract.functions.timeoutOf.return_value.call.return_value = 60 * 60 * 23
    net_time_left = calc_net_time_left(user.address)
    assert net_time_left == 60 * 60 * (23 - 24)


def test_net_value_positive(mocker, user):
    """
    Net balance should be positive and equal to to_wei(0.017 - 0.005, 'ether')
    """
    sum_outstanding_ious = mocker.patch('webserver.chain.sum_outstanding_ious')  # noqa: E501
    sum_outstanding_ious.return_value = 5
    contract = mocker.patch('webserver.chain.contract')
    contract.functions.price.return_value.call.return_value = to_wei(0.001, 'ether')  # noqa: E501
    contract.functions.balanceOf.return_value.call.return_value = to_wei(0.017, 'ether')  # noqa: E501
    net_balance = calc_net_balance(user.address)
    assert net_balance == to_wei(0.017 - 0.005, 'ether')


def test_net_value_zero(mocker, user):
    """
    Net balance should be zero and equal to to_wei(0.017 - 0.017, 'ether')
    """
    sum_outstanding_ious = mocker.patch('webserver.chain.sum_outstanding_ious')  # noqa: E501
    sum_outstanding_ious.return_value = 17
    contract = mocker.patch('webserver.chain.contract')
    contract.functions.price.return_value.call.return_value = to_wei(0.001, 'ether')  # noqa: E501
    contract.functions.balanceOf.return_value.call.return_value = to_wei(0.017, 'ether')  # noqa: E501
    net_balance = calc_net_balance(user.address)
    assert net_balance == to_wei(0.017 - 0.017, 'ether')
