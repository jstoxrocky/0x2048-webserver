from webserver.signing import (
    generate_gamecode,
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
        code = generate_gamecode()
        return code

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
    def update_game(address, current_state, update):
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
