import json
from webserver.game_info import (
    game_info as get_game_info,
)
from webserver.schemas import (
    GameInfos,
)


def test_happy_path(mocker):
    highscore = 10
    jackpot = 9

    Contract = mocker.patch('webserver.contract.Contract').return_value
    contract = Contract.new.return_value
    contract.functions.getHighscore.return_value.call.return_value = highscore
    contract.functions.getJackpot.return_value.call.return_value = jackpot

    info = json.loads(get_game_info())
    errors = GameInfos().validate(info)
    assert not errors
