import requests
from toolz import (
    compose,
)

fetch_rates = lambda: requests.get('https://api.gemini.com/v1/pricefeed')
parse_json = lambda x: x.json()
pred = lambda x: x['pair'] == 'ETHUSD'
filter_on_ethusd_pair = lambda x: filter(pred, x)
get_only_element = lambda x: x[0]
get_price = lambda x: x.get('price')
fetch_exchange_rate = compose(
    float,
    get_price,
    get_only_element,
    list,
    filter_on_ethusd_pair,
    parse_json,
    fetch_rates,
)
