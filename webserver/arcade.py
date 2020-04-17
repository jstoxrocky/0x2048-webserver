from webserver.signing import (
    random_32bytes,
    sign_score,
)
from webserver import (
    contract,
)


class Arcade():

    def __init__(self, player, game):
        self.player = player
        self.game = game

    @staticmethod
    def new_payment_code():
        payment_code = random_32bytes()
        return payment_code

    @staticmethod
    def new_session_id():
        session_id = random_32bytes()
        return session_id

    def confirm_payment(self, payment_code):
        error = contract.confirm_payment(
            self.game.id,
            self.player,
            payment_code,
        )
        return error

    def new_game(self):
        state = self.game.new()
        vrs = sign_score(self.game.id, self.player, state['score'])
        signed_score = {
            'v': vrs[0],
            'r': vrs[1],
            's': vrs[2],
        }
        return state, signed_score

    def update_game(self, current_state, update):
        state = self.game.update(current_state, update)
        vrs = sign_score(self.game.id, self.player, state['score'])
        signed_score = {
            'v': vrs[0],
            'r': vrs[1],
            's': vrs[2],
        }
        return state, signed_score
