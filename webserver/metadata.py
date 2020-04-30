import json
from webserver import (
    ethusd,
)
from toolz import (
    compose,
)
from web3 import (
    Web3,
)
from webserver import (
    contract,
)


to_json = lambda x: json.dumps(x)
exchange_rate = lambda: ethusd.fetch_exchange_rate()
format_as_currency = lambda x: '{:,.2f}'.format(x)
mult_exchange_rate = lambda x: x * exchange_rate()
to_usd = compose(format_as_currency, mult_exchange_rate)
format_eth = str
converge_currencies = lambda g: lambda h: lambda x: {'usd': g(x), 'eth': h(x)}
wei_to_ether = lambda x: Web3.fromWei(x, 'ether')
to_eth_usd = converge_currencies(to_usd)(format_eth)
to_eth = compose(float, wei_to_ether)
fetch_price = lambda contract: contract.get_price()
fetch_jackpot = lambda contract: contract.get_jackpot()
fetch_highscore = lambda contract: contract.get_highscore()
get_price = compose(to_eth_usd, to_eth, fetch_price)
get_jackpot = compose(to_eth_usd, to_eth, fetch_jackpot)
get_highscore = compose(str, fetch_highscore)
converge_metadata = lambda h: lambda j: lambda p: lambda c: {'highscore': h(c), 'jackpot': j(c), 'price': p(c)}  # noqa: E501
fetch_gamedata = converge_metadata(get_highscore)(get_jackpot)(get_price)
kontract = lambda: contract.arcade_contract()
get_metadata = compose(to_json, fetch_gamedata, kontract)
