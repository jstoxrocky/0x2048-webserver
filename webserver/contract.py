import json
from web3 import (
    Web3,
    HTTPProvider,
)
from webserver.config import (
    INFURA_TOKEN,
    ARCADE_ABI,
    ARCADE_ADDRESS,
)
from functools import (
    partial,
)
from web3._utils.transactions import (
    wait_for_transaction_receipt,
)

print(ARCADE_ADDRESS)
web3 = Web3(HTTPProvider('https://rinkeby.infura.io/%s' % (INFURA_TOKEN)))
contract = web3.eth.contract(
    abi=json.loads(ARCADE_ABI),
    address=ARCADE_ADDRESS,
)

wait_for_transaction_receipt = partial(wait_for_transaction_receipt, web3=web3)
