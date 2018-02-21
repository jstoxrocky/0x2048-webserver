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


def next_state(state, direction):
    board, score = state['board'], state['score']
    game = TwentyFortyEight.load(board, score)
    try:
        board, score = game.move(direction)
        gameover = False
    except GameOver:
        gameover = True
    state = {'board': game.board, 'score': game.score, 'gameover': gameover}
    return state
