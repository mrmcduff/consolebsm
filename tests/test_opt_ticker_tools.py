from app.utils import opt_ticker_tools as ot
from datetime import datetime


def test_ticker_price_string():
    assert ot.to_ticker_price(290.11) == "00290110"


def test_opt_type_to_ticker():
    assert ot.opt_type_to_ticker(ot.OptionType.CALL) == "C"
    assert ot.opt_type_to_ticker(ot.OptionType.PUT) == "P"


def test_create_option_tickers():
    call_ticker = ot.generate_option_ticker(
        "AAPL", datetime(2021, 11, 12), 50, ot.OptionType.CALL
    )
    put_ticker = ot.generate_option_ticker(
        "TSLA", datetime(2024, 1, 1), 375.75, ot.OptionType.PUT
    )
    assert call_ticker == "AAPL211112C00050000"
    assert put_ticker == "TSLA240101P00375750"
