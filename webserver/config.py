import os

# Public
ARCADE_ADDRESS = '0x607809129876B6637a291Ce2dEbA3D71c7ffc3E7'
ARCADE_ABI = '[{"inputs":[{"internalType":"bytes32","name":"gameId","type":"bytes32"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint8","name":"percentFee","type":"uint8"}],"name":"addGame","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"gameId","type":"bytes32"},{"internalType":"uint256","name":"score","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"claimHighscore","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"gameId","type":"bytes32"}],"name":"getHighscore","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"gameId","type":"bytes32"}],"name":"getJackpot","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"gameId","type":"bytes32"}],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"gameId","type":"bytes32"},{"internalType":"address","name":"addr","type":"address"}],"name":"getPaymentCode","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"gameId","type":"bytes32"}],"name":"getPercentFee","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"gameId","type":"bytes32"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"gameId","type":"bytes32"},{"internalType":"bytes32","name":"paymentCode","type":"bytes32"}],"name":"pay","outputs":[],"stateMutability":"payable","type":"function"}]'  # noqa: E501

# Private
REDIS_HOST = os.environ['HEROKU_REDIS_HOST']
REDIS_PORT = os.environ['HEROKU_REDIS_PORT']
REDIS_PASSWORD = os.environ['HEROKU_REDIS_PASSWORD']
PRIV = os.environ['PRIVATE_KEY_0x2048']
INFURA_PROJECT_ID = os.environ['INFURA_PROJECT_ID']
INFURA_PROJECT_SECRET = os.environ['INFURA_PROJECT_SECRET']
