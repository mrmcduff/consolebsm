EPSILON = 0.0001


def within_epsilon(actual: float, expected: float, epsilon: float = EPSILON) -> bool:
    return abs(actual - expected) < epsilon
