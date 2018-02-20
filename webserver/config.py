import os

ORIGINS = ['*']
PRIV = os.environ['ARCADE_PRIVATE_KEY']
ARCADE_ADDR = '0x8848c724B853307083F44526ad32C039b5ee1451'
ACCOUNT_ADDR = '0x8848c724b853307083f44526aD32c039B5eE1452'
INITIAL_STATE = {
    'board': [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    'score': 0,
    'gameover': True,
    'signature': {
        'message': '0x0',
        'messageHash': '0x0',
        'v': 0,
        'r': '0x0',
        's': '0x0',
        'signature': '0x0',
    },
}
