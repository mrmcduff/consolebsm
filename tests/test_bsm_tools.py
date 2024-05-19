from scipy import stats
from tests.test_tools import within_epsilon
from app.utils.bsm_tools import (
    calculate_d1,
    calculate_d2,
    calculate_bsm_call_price,
    calculate_bsm_put_price,
)


def test_sanity():
    assert within_epsilon(stats.norm.cdf(0), 0.5)


# This example comes from page 336 of OFOD, 10th ed
def test_known_values():
    actual_d1 = calculate_d1(
        stock_price=42, strike_price=40, rfr=0.1, sigma=0.2, time_in_years=0.5
    )
    actual_d2 = calculate_d2(d1=actual_d1, sigma=0.2, time_in_years=0.5)
    actual_call = calculate_bsm_call_price(
        stock_price=42, strike_price=40, rfr=0.1, sigma=0.2, time_in_years=0.5
    )
    actual_put = calculate_bsm_put_price(
        stock_price=42, strike_price=40, rfr=0.1, sigma=0.2, time_in_years=0.5
    )
    assert within_epsilon(actual_d1, 0.7693)
    assert within_epsilon(actual_d2, 0.6278)
    assert within_epsilon(actual_call, 4.76, 0.001)
    assert within_epsilon(actual_put, 0.81, 0.01)
