import requests
from eth_utils import (
    to_wei,
)


ETH_PRICE_URL = 'https://api.coinbase.com/v2/prices/ETH-USD/spot'


def get_price():
    params = {'currency': 'USD'}
    res = requests.get(ETH_PRICE_URL, params=params)
    eth_price_data = res.json()
    price = eth_price_data['data']['amount']
    return float(price)


def flip_xe(rate):
    return 1 / rate


def to_wei_per_dollar(dollars_per_eth):
    eth_per_dollars = flip_xe(dollars_per_eth)
    price = to_wei(eth_per_dollars, 'ether')
    return price
