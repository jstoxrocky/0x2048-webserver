from webserver.signing import (
    random_32bytes,
    sign_score,
)
from webserver import (
    contract,
)
from game.game import (
    TwentyFortyEight
)
from webserver.exceptions import (
    PaymentError,
)


class Arcade():

    def __init__(self, player):
        self.player = player

    @staticmethod
    def new_gamecode():
        gamecode = random_32bytes()
        return gamecode

    @staticmethod
    def new_session_id():
        session_id = random_32bytes()
        return session_id

    @staticmethod
    def confirm_payment(address, gamecode):
        confirmed = contract.confirm_payment(address, gamecode)
        error = None
        if not confirmed:
            error = PaymentError
        return error

    def new_game(self):
        state = TwentyFortyEight.new()
        signed_score = sign_score(self.player, state['score'])
        signature = {
            'v': signed_score['v'],
            'r': signed_score['r'],
            's': signed_score['s'],
        }
        return state, signature

    def update_game(self, current_state, update):
        state = TwentyFortyEight.update(current_state, update)
        signed_score = sign_score(self.player, state['score'])
        signature = {
            'v': signed_score['v'],
            'r': signed_score['r'],
            's': signed_score['s'],
        }
        return state, signature
