from dataclasses import dataclass
from typing import List


@dataclass
class OhlcResult:
    c: float  # close
    h: float  # high
    l: float  #noqa E741
    o: float  # open
    t: float  # millisecond timestamp for end of the window
    v: float  # trading volume during the time period
    vw: float | None = None  # the volume-weighted average
    n: float | None = None  # number of transactions in aggregate window
    otc: bool = False  # whether or not this is for an otc ticker - false if not present


@dataclass
class RangeOhlc:
    ticker: str
    adjusted: bool
    queryCount: int
    request_id: int
    results: List[OhlcResult]
    resultsCount: int
    status: str
    next_url: str | None = None


# {
#   "adjusted": true,
#   "next_url": "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/1578114000000/2020-01-10?cursor=bGltaXQ9MiZzb3J0PWFzYw",
#   "queryCount": 2,
#   "request_id": "6a7e466379af0a71039d60cc78e72282",
#   "results": [
#     {
#       "c": 75.0875,
#       "h": 75.15,
#       "l": 73.7975,
#       "n": 1,
#       "o": 74.06,
#       "t": 1577941200000,
#       "v": 135647456,
#       "vw": 74.6099
#     },
#     {
#       "c": 74.3575,
#       "h": 75.145,
#       "l": 74.125,
#       "n": 1,
#       "o": 74.2875,
#       "t": 1578027600000,
#       "v": 146535512,
#       "vw": 74.7026
#     }
#   ],
#   "resultsCount": 2,
#   "status": "OK",
#   "ticker": "AAPL"
# }
