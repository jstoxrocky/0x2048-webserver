ORIGINS = ['*']
PRIV = b'\x11' * 32
ADDR = '0xc305c901078781C232A2a521C2aF7980f8385ee9'
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
        'message': '',
        'messageHash': '',
        'v': 0,
        'r': 0,
        's': 0,
        'signature': '',
    },
}
