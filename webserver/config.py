import os

ORIGINS = ['*']
PRIV = os.environ['PRIVATE_KEY_0x2048']
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
DISCLAIMER = 'This signature is for intended for use with 0x2048 at the below Rinkeby address. If you are seeing this message and not interacting with 0x2048, someone may be attempting forge your signature'  # noqa: E501
