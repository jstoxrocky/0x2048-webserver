import json
from webserver.metadata import (
    get_metadata,
)


class MockContract():

    @staticmethod
    def get_highscore():
        return 17

    @staticmethod
    def get_price():
        return 1000000000000000

    @staticmethod
    def get_jackpot():
        return 4000000000000000


def test_happy_path(mocker, monkeypatch):
    expected_metadata = {
        'highscore': '17',
        'jackpot': {
            'eth': '0.004',
            'usd': '0.80',
        },
        'price': {
            'eth': '0.001',
            'usd': '0.20',
        },
    }
    mocker.patch('webserver.metadata.ethusd.fetch_exchange_rate').return_value = 200.00   # noqa: E501
    mocker.patch('webserver.metadata.contract.arcade_contract').return_value = MockContract   # noqa: E501
    response = get_metadata()
    metadata = json.loads(response)
    assert metadata == expected_metadata
