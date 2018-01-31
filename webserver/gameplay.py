from webserver.exceptions import (
    UnknownMove,
)
from game.mechanics import (
    UP, DOWN, LEFT, RIGHT,
)
from game.game import (
    TwentyFortyEight
)
from game.exceptions import (
    GameOver,
)


def new():
    game = TwentyFortyEight.new(4, 4)
    gamestate = {'board': game.board, 'score': 0, 'gameover': False}
    return gamestate


def load_and_play(state, direction):
    if direction not in {UP, DOWN, LEFT, RIGHT}:
        raise UnknownMove
    board, score = state['board'], state['score']
    game = TwentyFortyEight.load(board, score)
    try:
        board, score = game.move(direction)
    except GameOver:
        gameover = True
    gameover = gameover or state['gameover']
    state = {'board': game.board, 'score': game.score, 'gameover': gameover}
    return state
