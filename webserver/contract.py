import os
import arcade_protocol
from game.game import (
    TwentyFortyEight,
)
from web3.providers import (
    HTTPProvider,
)
from webserver.config import (
    ADDRESS,
    ABI,
)


infura_project_id = os.environ['INFURA_PROJECT_ID']
infura_project_secret = os.environ['INFURA_PROJECT_SECRET']
headers = {"auth": ("", infura_project_secret)}
uri = 'https://ropsten.infura.io/v3/%s' % (infura_project_id)
provider = HTTPProvider(uri, headers)
game_id = TwentyFortyEight.id
arcade_contract = lambda: arcade_protocol.Contract(
    provider,
    ADDRESS,
    ABI,
    game_id,
)
