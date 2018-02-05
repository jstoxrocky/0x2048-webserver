from webserver.price import (
    get_price,
)


def test_get_price():
    output = get_price()
    assert isinstance(output, float)
    assert output >= 0
