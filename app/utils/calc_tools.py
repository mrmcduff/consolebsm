from typing import List
import math
import functools


def get_geo_avg(values: List[float]) -> float:
    if any(map(lambda v: v <= 0, values)):
        return 0
    logsum = functools.reduce(lambda cm, v: cm + math.log(v), values, 0)
    return math.exp(logsum / len(values))
