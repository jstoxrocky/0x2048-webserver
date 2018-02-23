import pytest
from webserver.application import (
    application,
)
from webserver.state_channel import (
    solidity_keccak,
    sign,
)
from webserver.config import (
    ACCOUNT_ADDR,
    ARCADE_ADDR,
    PRIV,
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
            sess['has_paid'] = True


@pytest.fixture(scope="function")
def session_has_not_paid(app):
    with app as c:
        with c.session_transaction() as sess:
            sess['has_paid'] = False


@pytest.fixture(scope="function")
def iou_data(app, user):
    value = 8
    msg = solidity_keccak(ACCOUNT_ADDR, user.address, value)
    signature = sign(msg, user.privateKey)
    payload = {
        'user': user.address,
        'value': value,
        'signature': signature,
    }
    return payload


@pytest.fixture(scope="function")
def gamestate_data(app, user):
    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    gameover = True
    score = 8
    msg = solidity_keccak(ARCADE_ADDR, user.address, score)
    signature = sign(msg, PRIV)
    payload = {
        'score': score,
        'board': board,
        'gameover': gameover,
        'signature': signature,
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
