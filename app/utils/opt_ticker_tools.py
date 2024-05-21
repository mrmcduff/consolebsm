from datetime import datetime
import math
from enum import StrEnum
from .date_tools import format_option_ticker_date

OptionType = StrEnum("Option", ["PUT", "CALL"])


def generate_option_ticker(
    equity_ticker: str,
    maturity_date: datetime,
    strike_price: float,
    opt_type: OptionType,
) -> str:
    # Note: not yet correctly formatting the strike price and the option type
    return f"{equity_ticker}{format_option_ticker_date(maturity_date)}{opt_type_to_ticker(opt_type)}{to_ticker_price(strike_price)}"


def opt_type_to_ticker(opt_type: OptionType) -> str:
    return "C" if opt_type == OptionType.CALL else "P"


def to_ticker_price(strike_price: float) -> str:
    return f"{(math.floor(strike_price * 1000)):08d}"
