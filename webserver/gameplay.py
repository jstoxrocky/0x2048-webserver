from game.game import (
    TwentyFortyEight
)
from game.exceptions import (
    GameOver,
)


def new():
    game = TwentyFortyEight.new(4, 4)
    new_state = {'board': game.board, 'score': 0, 'gameover': False}
    return new_state


def next_state(state, direction):
    board, score = state['board'], state['score']
    game = TwentyFortyEight.load(board, score)
    try:
        board, score = game.move(direction)
        gameover = False
    except GameOver:
        board, score = game.board, game.score
        gameover = True
    new_state = {'board': board, 'score': score, 'gameover': gameover}
    return new_state
