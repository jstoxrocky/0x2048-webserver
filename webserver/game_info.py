import json
from webserver.arcade import (
    Arcade,
)
from webserver.game_config import (
    GAME_IDS,
)


def game_info():
    info = map(Arcade.game_info, GAME_IDS)
    games = {'games': list(info)}
    return json.dumps(games)
