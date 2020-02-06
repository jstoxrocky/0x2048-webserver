import os

ORIGINS = ['*']
PRIV = os.environ['PRIVATE_KEY_0x2048']
ARCADE_ADDRESS = os.environ['ARCADE_ADDRESS']
ARCADE_ABI = '[{"constant": true, "inputs": [], "name": "round", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [{"name": "addr", "type": "address"}], "name": "getNonce", "outputs": [{"name": "", "type": "bytes32"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "v", "type": "uint8"}, {"name": "r", "type": "bytes32"}, {"name": "s", "type": "bytes32"}, {"name": "user", "type": "address"}, {"name": "score", "type": "uint256"}], "name": "uploadScore", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "jackpot", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [{"name": "", "type": "address"}], "name": "nonces", "outputs": [{"name": "", "type": "bytes32"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": false, "inputs": [{"name": "nonce", "type": "bytes32"}], "name": "pay", "outputs": [], "payable": true, "stateMutability": "payable", "type": "function"}, {"constant": true, "inputs": [], "name": "highscore", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "payable": false, "stateMutability": "view", "type": "function"}, {"constant": true, "inputs": [], "name": "price", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}, {"inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor"}]'  # noqa: E501
INFURA_TOKEN = os.environ['INFURA_ACCESS_TOKEN']
INITIAL_STATE = {
    'board': [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    'gameover': True,
    'score': 0,
    'signature': {
        'messageHash': '0x0',
        'v': 0,
        'r': 0,
        's': 0,
        'signature': '0x0',
    },
    'recoveredAddress': ARCADE_ADDRESS,
}
DISCLAIMER = 'This signature is for intended for use with 0x2048 at the below Rinkeby address. If you are seeing this message and not interacting with 0x2048, someone may be attempting forge your signature'  # noqa: E501
