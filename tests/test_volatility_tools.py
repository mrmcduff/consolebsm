from app.utils import volatility_tools as vt
from tests.test_tools import within_epsilon
import pytest
import math


def setup_known_values():
    closes = [
        100,
        104,
        103.2,
        102.2,
        102.8,
        103.4,
        101,
        105,
        105.5,
        104.3,
        101.9,
        102,
        102,
        104.4,
        105.5,
    ]

    uis = [
        0.039220713,
        -0.007722046,
        -0.009737175,
        0.005853675,
        0.005819609,
        -0.023484445,
        0.038839833,
        0.004750603,
        -0.011439591,
        -0.023279422,
        0.000980873,
        0,
        0.023256862,
        0.010481277,
    ]

    sum_squared = 0.002866614
    sum_squares = 0.005167957
    first_term = 0.00036914
    second_term = 1.36505e-05
    s = math.sqrt(first_term - second_term)
    tau = 1 / 252
    sigma = s / math.sqrt(tau)
    err = sigma / math.sqrt(2 * len(closes))
    return {
        "closes": closes,
        "vals": list(map(lambda cl: {"c": cl}, closes)),
        "uis": uis,
        "sum_squared": sum_squared,
        "sum_squares": sum_squares,
        "sigma": sigma,
        "tau": tau,
        "err": err,
    }


def test_sum_squares():
    ans = vt.sum_squares([1, 2, 3, 4])
    assert ans == 1 + 4 + 9 + 16


def test_known_sum_squares():
    knowns = setup_known_values()
    assert within_epsilon(vt.sum_squares(knowns["uis"]), knowns["sum_squares"]) is True


def test_sum_squared():
    ans = vt.sum_squared([1, 2, 3, 4, 5])
    assert ans == 15**2


def test_known_sum_squared():
    knowns = setup_known_values()
    assert within_epsilon(vt.sum_squared(knowns["uis"]), knowns["sum_squared"]) is True


def test_validate_valids():
    assert vt.validate_numbers([1, 3, 777777, 4e7, 0.000122, 1e-3])


def test_validate_negatives():
    with pytest.raises(ValueError):
        vt.validate_numbers([1, 3, -2])


def test_validate_zeros():
    with pytest.raises(ValueError):
        vt.validate_numbers([55, 1e4, 0, 12])


def test_get_uis_length():
    uis = vt.get_uis([2, 3, 4, 5])
    assert len(uis) == 3
    assert min(uis) > 0


def test_get_uis():
    knowns = setup_known_values()
    act_uis = vt.get_uis(knowns["closes"])
    exp_uis = knowns["uis"]
    for index, ui in enumerate(act_uis):
        assert within_epsilon(ui, exp_uis[index]) is True


def test_validate_valid_keys():
    test_list = [{"a": 1, "b": 2}, {"a": "foo", "x": 13, "c": 12}]
    test_list_with_c = [{"a": 1, "c": 2}, {"a": "foo", "c": 13}]
    assert vt.validate_key(test_list, "a") is True
    assert vt.validate_key(test_list, "x") is False
    assert vt.validate_key(test_list_with_c, "c") is True


def test_invalid_length():
    short_list = [{"a": 1, "b": 2}]
    empty_list = []
    with pytest.raises(ValueError):
        vt.calculate_daily_volatility(short_list)
    with pytest.raises(ValueError):
        vt.calculate_daily_volatility(empty_list)


def test_invalid_keys():
    test_list = [{"a": 1, "b": 2}, {"a": 12, "x": 13, "c": 12}]
    test_list_with_c = [{"a": 1, "c": 2}, {"a": 12, "c": 13}]
    with pytest.raises(ValueError):
        vt.calculate_daily_volatility(test_list)
    with pytest.raises(ValueError):
        vt.calculate_daily_volatility(test_list_with_c, "b")


def test_simple_values():
    test_list = [{"o": 1, "h": 2, "l": 3, "c": 4}, {"o": 1, "h": 2, "l": 3, "c": 4}]
    [sigma, err] = vt.calculate_daily_volatility(test_list)
    assert sigma == 0
    assert err == 0


# def test_calculate_known_tau():
#   knowns = setup_known_values()
#   tau = vt.calculate_tau(knowns['vals'])
#   assert within_epsilon(tau, knowns['tau']) is True


def test_known_values():
    knowns = setup_known_values()
    [sigma, err] = vt.calculate_daily_volatility(knowns["vals"])
    assert within_epsilon(sigma, knowns["sigma"]) is True
    assert within_epsilon(err, knowns["err"]) is True
