import pytest
from webserver.application import (
    application,
)
from webserver.state_channel import (
    solidity_keccak,
    sign,
)
from webserver.config import (
    ARCADE_ADDR,
)
from game.game import (
    TwentyFortyEight,
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
def session_has_paid(app):
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = True


@pytest.fixture(scope="function")
def session_has_not_paid(app):
    with app as c:
        with c.session_transaction() as sess:
            sess['paid'] = False


@pytest.fixture(scope="function")
def signature_data(app, user):
    nonce = 8
    msg = solidity_keccak(ARCADE_ADDR, user.address, nonce)
    signature = sign(msg, user.privateKey)
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
        'signature': signature_data,
    }
    return payload


@pytest.fixture(scope="function")
def move_data(app, user):
    direction = 1
    payload = {
        'user': user.address,
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
