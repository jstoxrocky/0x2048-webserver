import os

REDIS_HOST = os.environ['HEROKU_REDIS_HOST']
REDIS_PORT = os.environ['HEROKU_REDIS_PORT']
REDIS_PASSWORD = os.environ['HEROKU_REDIS_PASSWORD']
PRIV = os.environ['PRIVATE_KEY_0x2048']
ARCADE_ADDRESS = os.environ['ARCADE_ADDRESS']
ARCADE_ABI = '[{"inputs": [], "stateMutability": "nonpayable", "type": "constructor"}, {"inputs": [{"internalType": "address", "name": "addr", "type": "address"}], "name": "getNonce", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "highscore", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "jackpot", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "nonces", "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "bytes32", "name": "nonce", "type": "bytes32"}], "name": "pay", "outputs": [], "stateMutability": "payable", "type": "function"}, {"inputs": [], "name": "price", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "round", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint8", "name": "v", "type": "uint8"}, {"internalType": "bytes32", "name": "r", "type": "bytes32"}, {"internalType": "bytes32", "name": "s", "type": "bytes32"}, {"internalType": "uint256", "name": "score", "type": "uint256"}], "name": "uploadScore", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'  # noqa: E501
INFURA_PROJECT_ID = os.environ['INFURA_PROJECT_ID']
INFURA_PROJECT_SECRET = os.environ['INFURA_PROJECT_SECRET']
PROVIDER_HEADERS = {"auth": ("", INFURA_PROJECT_SECRET)}
PROVIDER_URI = 'https://ropsten.infura.io/v3/%s' % (INFURA_PROJECT_ID)
