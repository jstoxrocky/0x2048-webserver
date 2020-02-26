from webserver.signing import (
    nonce,
    recover_challenge_signer,
    sign_score,
)
from webserver.contract import (
    confirm_payment,
)
from game.game import (
    TwentyFortyEight
)


class Arcade():

    def __init__(self, player_address):
        self.player_address = player_address

    @staticmethod
    def new_session():
        session_id = nonce()
        challenge = nonce()
        return {
            'session_id': session_id,
            'challenge': challenge,
        }

    @staticmethod
    def confirm_payment(challenge, v, r, s):
        recovered_address = recover_challenge_signer(challenge, v, r, s)
        confirmed = confirm_payment(recovered_address, challenge)
        success = True
        if not confirmed:
            success = False
        return {
            'recovered_address': recovered_address,
            'success': success
        }

    def new_game(self):
        state = TwentyFortyEight.new()
        signed_score = sign_score(self.player_address, state['score'])
        return {
            'state': state,
            'signed_score': {
                'v': signed_score['v'],
                'r': signed_score['r'],
                's': signed_score['s'],
            }
        }

    def update_game(self, current_state, update):
        state = TwentyFortyEight.update(current_state, update)
        signed_score = sign_score(self.player_address, state['score'])
        return {
            'state': state,
            'signed_score': {
                'v': signed_score['v'],
                'r': signed_score['r'],
                's': signed_score['s'],
            }
        }
