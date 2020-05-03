import json
from webserver.metadata import (
    get_metadata,
)


def test_happy_path(mocker, mock_contract):
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
    mocker.patch('webserver.metadata.contract.arcade_contract').return_value = mock_contract   # noqa: E501
    response = get_metadata()
    metadata = json.loads(response)
    assert metadata == expected_metadata
