import requests
from eth_utils import (
    to_wei,
)


ETH_PRICE_URL = 'https://api.coinbase.com/v2/prices/ETH-USD/spot'


def get_price_of_eth_in_dollars():
    params = {'currency': 'USD'}
    res = requests.get(ETH_PRICE_URL, params=params)
    eth_price_data = res.json()
    price = eth_price_data['data']['amount']
    return float(price)


def get_current_dollar_price_in_wei():
    dollars_per_eth = get_price_of_eth_in_dollars()
    eth_per_dollars = 1 / dollars_per_eth
    price = to_wei(eth_per_dollars, 'ether')
    return price
