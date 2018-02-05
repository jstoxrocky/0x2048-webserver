from webserver.price import (
    flip_xe,
    to_wei_per_dollar,
    get_price,
)
from unittest.mock import (
    patch,
)
from requests import (
    Response,
)
import io
import json


def test_flix_xe():
    val = 3465
    output = flip_xe(val)
    assert output == 0.0002886002886002886


def test_to_wei_per_dollar():
    val = 1400
    output = to_wei_per_dollar(val)
    assert output == 714285714285714


@patch('webserver.price.requests.get')
def test_get_price(mocked):
    response = Response()
    data = {'data': {'amount': 1700}}
    response.raw = io.BytesIO(json.dumps(data).encode())
    mocked.return_value = response
    output = get_price()
    assert output == 1700
