import math
from typing import List, Tuple
from scipy import stats


def validate_nonzeros(*nonzeros: float) -> Tuple[bool, List[float]]:
    zeros = [z for z in nonzeros if z == 0]
    return [len(zeros) == 0, zeros]


def calculate_d1(
    stock_price: float,
    strike_price: float,
    rfr: float,
    sigma: float,
    time_in_years: float,
) -> float:
    [valid, _] = validate_nonzeros(strike_price, sigma, time_in_years)
    if not valid:
        raise ValueError("Strike price, sigma, and time must all be nonzero")

    denominator = sigma * math.sqrt(time_in_years)
    stock_to_strike_term = math.log(stock_price / strike_price)
    rate_and_vol_term = time_in_years * (rfr + 0.5 * sigma**2)

    return (stock_to_strike_term + rate_and_vol_term) / denominator


def calculate_d2(d1: float, sigma: float, time_in_years: float) -> float:
    return d1 - sigma * math.sqrt(time_in_years)


def calculate_strike_pv(strike_price: float, rfr: float, time_in_years: float) -> float:
    return strike_price * math.exp(-1 * rfr * time_in_years)


def calculate_bsm_call_price(
    stock_price: float,
    strike_price: float,
    rfr: float,
    sigma: float,
    time_in_years: float,
) -> float:
    d1 = calculate_d1(stock_price, strike_price, rfr, sigma, time_in_years)
    d2 = calculate_d2(d1, sigma, time_in_years)
    spv = calculate_strike_pv(
        strike_price=strike_price, rfr=rfr, time_in_years=time_in_years
    )
    nd1 = stats.norm.cdf(d1)
    nd2 = stats.norm.cdf(d2)
    return stock_price * nd1 - spv * nd2


def calculate_bsm_put_price(
    stock_price: float,
    strike_price: float,
    rfr: float,
    sigma: float,
    time_in_years: float,
) -> float:
    d1 = calculate_d1(stock_price, strike_price, rfr, sigma, time_in_years)
    d2 = calculate_d2(d1, sigma, time_in_years)
    spv = calculate_strike_pv(
        strike_price=strike_price, rfr=rfr, time_in_years=time_in_years
    )
    ndm2 = stats.norm.cdf(-1 * d2)
    ndm1 = stats.norm.cdf(-1 * d1)
    return spv * ndm2 - stock_price * ndm1
