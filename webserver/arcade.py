from webserver.signing import (
    random_32bytes,
    sign_score,
)
from webserver import (
    contract,
)
from webserver.game_config import (
    GAME_MAPPING,
    GAME_METADATA,
)


class Arcade():

    def __init__(self, player):
        self.player = player

    @staticmethod
    def game_info(game_id):
        meta = GAME_METADATA[game_id]
        stats = contract.get_game_stats(game_id)
        result = {**meta, **stats, 'id': game_id}
        return result

    @staticmethod
    def new_payment_code():
        payment_code = random_32bytes()
        return payment_code

    @staticmethod
    def new_session_id():
        session_id = random_32bytes()
        return session_id

    @staticmethod
    def confirm_payment(game_id, address, payment_code):
        error = contract.confirm_payment(game_id, address, payment_code)
        return error

    def new_game(self, game_id):
        game = GAME_MAPPING[game_id]
        state = game.new()
        vrs = sign_score(game_id, self.player, state['score'])
        signed_score = {
            'v': vrs[0],
            'r': vrs[1],
            's': vrs[2],
        }
        return state, signed_score

    def update_game(self, game_id, current_state, update):
        game = GAME_MAPPING[game_id]
        state = game.update(current_state, update)
        vrs = sign_score(game_id, self.player, state['score'])
        signed_score = {
            'v': vrs[0],
            'r': vrs[1],
            's': vrs[2],
        }
        return state, signed_score
