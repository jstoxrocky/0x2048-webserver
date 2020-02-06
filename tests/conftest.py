import pytest
from webserver.application import (
    application,
)
from webserver.signing import (
    sign_score,
)
from webserver.config import (
    ARCADE_ADDRESS,
)
from game.game import (
    TwentyFortyEight,
)
from eth_utils import (
    encode_hex,
    keccak,
)


@pytest.fixture(scope="module")
def app():
    app = application.test_client()
    app.testing = True
    return app


@pytest.fixture(scope="function")
def new_game(request, app):
    with app.session_transaction() as sess:
        sess['gameover'] = False
        game = TwentyFortyEight.new(4, 4)
        sess['score'] = game.score
        sess['board'] = game.board

    def resource_a_teardown():
        with app.session_transaction() as sess:
            sess['gameover'] = True
    request.addfinalizer(resource_a_teardown)


@pytest.fixture(scope="module")
def api_prefix():
    return '/api/v1'


@pytest.fixture(scope="function")
def signature_data(app, user):
    nonce = 8
    signature = sign_score(user.key, ARCADE_ADDRESS, user.address, nonce)
    return signature


@pytest.fixture(scope="function")
def gamestate_data(app, user, signature_data):
    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    gameover = True
    score = 8  # Comes from signature_data
    payload = {
        'score': score,
        'board': board,
        'gameover': gameover,
    }
    return payload


@pytest.fixture(scope="function")
def signed_gamestate_data(app, gamestate_data, user, signature_data):
    gamestate_data['signature'] = signature_data
    gamestate_data['recoveredAddress'] = user.address
    return gamestate_data


@pytest.fixture(scope="function")
def move_data(app):
    direction = 1
    payload = {
        'direction': direction,
    }
    return payload


@pytest.fixture(scope="function")
def nonce_data(app, user):
    nonce = '0x123456'
    payload = {
        'nonce': nonce,
    }
    return payload


@pytest.fixture(scope="function")
def receipt_data(app, user, signature_data):
    payload = {
        'signature': signature_data['signature'],
        'txhash': encode_hex(keccak(b'')),
    }
    return payload
