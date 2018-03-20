import os
import json
from web3 import (
    Web3,
    HTTPProvider,
)


ACCOUNT_ABI = '[{"constant": true, "inputs": [{"name": "", "type": "address"}], "name": "iousCount", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [{"name": "", "type": "address"}], "name": "balances", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [{"name": "user", "type": "address"}], "name": "getNonce", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "v", "type": "uint8"}, {"name": "r", "type": "bytes32"}, {"name": "s", "type": "bytes32"}, {"name": "schemaHash", "type": "bytes32"}, {"name": "user", "type": "address"}, {"name": "nonce", "type": "uint256"}], "name": "finalizeIOU", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [{"name": "_addr", "type": "address"}], "name": "timeoutOf", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "withdraw", "outputs": [], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "oneWeek", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [{"name": "_addr", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "price", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [], "name": "deposit", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}, {"constant": true, "inputs": [{"name": "", "type": "address"}], "name": "timeouts", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}]'  # noqa: E501
ACCOUNT_ADDRESS = os.environ['ACCOUNT_ADDRESS']
INFURA_TOKEN = os.environ['INFURA_ACCESS_TOKEN']


web3 = Web3(HTTPProvider('https://rinkeby.infura.io/%s' % (INFURA_TOKEN)))
contract = web3.eth.contract(
    abi=json.loads(ACCOUNT_ABI),
    address=ACCOUNT_ADDRESS,
)
