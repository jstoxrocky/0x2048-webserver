from webserver.db import (
    sum_outstanding_ious,
)
from webserver.contract import (
    contract,
)


PRICE = 0
WALLET_BALANCE = 0
TIME_LEFT = 0


def calc_net_time_left(user):
    buffer_period = 60 * 60 * 24 * 1  # One day
    time_left = contract.functions.timeoutOf(user).call()
    net_time_left = time_left - buffer_period
    return net_time_left


def calc_net_balance(user):
    count = sum_outstanding_ious(user)
    price = contract.functions.price().call()
    iou_balance = count * price
    wallet_balance = contract.functions.balanceOf(user).call()
    net_balance = wallet_balance - iou_balance
    return net_balance
