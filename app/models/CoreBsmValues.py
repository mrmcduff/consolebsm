from dataclasses import dataclass


@dataclass
class CoreBsmValues:
    ticker: str | None = None
    days: int | None = None
    end_date_str: str | None = None
    start_date_str: str | None = None
    risk_free_rate: float | None = None
    strike_price: float | None = None
    volatility: float | None = None
