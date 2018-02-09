import os

ORIGINS = ['*']
PRIV = os.environ['ARCADE_PRIVATE_KEY']
ADDR = '0x2E26Cc06B0aB12C01a7F8D805d95c14D5D886f96'
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
