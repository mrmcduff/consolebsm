from typing import List, Dict, Union
import math

TRADE_DAYS_PER_YEAR = 252

def sum_squares(vals: List[float]) -> float:
  return sum([x**2 for x in vals])

def sum_squared(vals: List[float]) -> float:
  return sum(vals)**2

def validate_numbers(vals: List[float]) -> bool:
  for v in vals:
    if v <= 0:
      raise ValueError('All values must be greater than zero')
  return True

def get_uis(vals: List[float]) -> List[float]:
  previous_vals = vals[:-1]
  next_vals = vals[1:]
  uis = map(lambda nv: math.log(nv[1]/previous_vals[nv[0]]), enumerate(next_vals))
  return list(uis)

def validate_key(items: List[Dict], key: str) -> bool:
  return all(key in li for li in items)

def calculate_tau(items: List) -> float:
  return len(items) / TRADE_DAYS_PER_YEAR

def calculate_volatility(vals: List[float]) -> tuple[float, float]:
  count = len(vals)
  uis = get_uis(vals)
  uis_squared = sum_squares(uis)
  sum_uis_squared = sum_squared(uis)
  first_term = (1/(count - 1)) * uis_squared
  second_term = (1/(count*(count - 1)))* sum_uis_squared
  s = math.sqrt(first_term - second_term)
  tau = calculate_tau(vals)
  sigma_hat = s / math.sqrt(tau)
  error = sigma_hat / math.sqrt(2*count)
  return sigma_hat, error


def calculate_daily_volatility(items: List[Dict], key: str = 'c') -> tuple[float, float]:
  count = len(items)
  if count <= 1:
    raise ValueError('Cannot calculate volatility of only one value')
  if not validate_key(items, key):
    raise ValueError(f'Key {key} must be present in all inputs')

  vals = list(map(lambda item: item[key], items))
  return calculate_volatility(vals)
