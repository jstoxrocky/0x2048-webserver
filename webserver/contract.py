import json
from web3 import (
    Web3,
    HTTPProvider,
)
from webserver.config import (
    PROVIDER_URI,
    PROVIDER_HEADERS,
    ARCADE_ADDRESS,
    ARCADE_ABI,
)


class Contract():

    def __init__(self, uri, headers):
        self.web3 = Web3(HTTPProvider(uri, headers))

    def new(self, address, abi):
        contract = self.web3.eth.contract(
            abi=json.loads(abi),
            address=address,
        )
        return contract


def confirm_payment(signer, gamecode):
    arcade_contract = Contract(
        PROVIDER_URI,
        PROVIDER_HEADERS
    ).new(ARCADE_ADDRESS, ARCADE_ABI)
    gamecode_in_contract = arcade_contract.functions.getNonce(signer).call()
    return gamecode_in_contract == gamecode
