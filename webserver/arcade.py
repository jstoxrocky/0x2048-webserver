from webserver.signing import (
    random_32bytes,
    recover_gamecode_signer,
    sign_score,
)
from webserver.contract import (
    confirm_payment,
)
from game.game import (
    TwentyFortyEight
)


class Arcade():

    def __init__(self):
        pass

    @staticmethod
    def new_gamecode():
        gamecode = random_32bytes()
        return gamecode

    @staticmethod
    def new_session_id():
        session_id = random_32bytes()
        return session_id

    @staticmethod
    def recover_signer(gamecode, v, r, s):
        recovered_address = recover_gamecode_signer(gamecode, v, r, s)
        return recovered_address

    @staticmethod
    def confirm_payment(address, gamecode):
        confirmed = confirm_payment(address, gamecode)
        success = True
        if not confirmed:
            success = False
        return success

    @staticmethod
    def new_game(address):
        state = TwentyFortyEight.new()
        signed_score = sign_score(address, state['score'])
        return {
            'state': state,
            'signed_score': {
                'v': signed_score['v'],
                'r': signed_score['r'],
                's': signed_score['s'],
            }
        }

    @staticmethod
    def update_game(current_state, update, address):
        state = TwentyFortyEight.update(current_state, update)
        signed_score = sign_score(address, state['score'])
        return {
            'state': state,
            'signed_score': {
                'v': signed_score['v'],
                'r': signed_score['r'],
                's': signed_score['s'],
            }
        }
