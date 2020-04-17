import json
from web3 import (
    Web3,
    HTTPProvider,
)
from webserver.config import (
    INFURA_PROJECT_SECRET,
    INFURA_PROJECT_ID,
    ARCADE_ADDRESS,
    ARCADE_ABI,
)
from hexbytes import (
    HexBytes,
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


def confirm_payment(game_id, address, payment_code):
    provider_header = {"auth": ("", INFURA_PROJECT_SECRET)}
    provider_uri = 'https://ropsten.infura.io/v3/%s' % (INFURA_PROJECT_ID)
    arcade_contract = Contract(
        provider_uri,
        provider_header
    ).new(ARCADE_ADDRESS, ARCADE_ABI)
    bytes_payment_code = arcade_contract.functions.getPaymentCode(
        game_id,
        address,
    ).call()
    payment_code_in_contract = HexBytes(bytes_payment_code).hex()
    confirmed = payment_code_in_contract == payment_code
    error = not confirmed
    return error
