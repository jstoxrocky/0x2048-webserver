import pytest
from webserver.application import (
    application,
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
