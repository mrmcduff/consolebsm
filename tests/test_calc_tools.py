from app.utils.calc_tools import get_geo_avg
from tests.test_tools import within_epsilon


def test_geo_avg():
    vals = [1, 4]
    result = get_geo_avg(vals)
    assert within_epsilon(result, 2)


def test_slightly_longer_geo_avg():
    assert within_epsilon(get_geo_avg([1, 3, 9]), 3)
