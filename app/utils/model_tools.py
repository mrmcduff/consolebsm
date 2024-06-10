from app.models.RangeOhlc import RangeOhlc, OhlcResult
from typing import Any, List, Literal, Tuple, get_args
from dataclasses import asdict

EXPECTED_KEYS = [
    "adjusted",
    "queryCount",
    "results",
    "resultsCount",
    "status",
    "ticker",
    "request_id",
]

literal_keys = Literal["o", "h", "l", "c", "t", "v"]
EXPECTED_RESULT_KEYS: Tuple[literal_keys, ...] = get_args(literal_keys)


def get_range_values(rangeOhlc: RangeOhlc, key: literal_keys) -> List[float]:
    return [*map(lambda ob: asdict(ob)[key], rangeOhlc.results)]


def range_ohlc_from_json(data: Any) -> RangeOhlc | None:
    if "status" in data and data["status"] != "OK":
        return None
    for key in EXPECTED_KEYS:
        if key not in data:
            raise ValueError(f"Missing expected json key {key}")

    results_raw = data["results"]
    if not isinstance(results_raw, list):
        raise ValueError("Results are not list type")
    results = list(map(ohlc_result_from_json, results_raw))
    rangeOhlc = RangeOhlc(
        ticker=data["ticker"],
        adjusted=data["adjusted"],
        queryCount=data["queryCount"],
        results=results,
        request_id=data["request_id"],
        resultsCount=data["resultsCount"],
        status=data["status"],
    )
    if "next_url" in data:
        rangeOhlc.next_url = data["next_url"]

    return rangeOhlc


def ohlc_result_from_json(data: Any) -> OhlcResult:
    for key in EXPECTED_RESULT_KEYS:
        if key not in data:
            raise ValueError(f"Result data missing expected json key {key}")
    ohlc = OhlcResult(
        c=data["c"], h=data["h"], l=data["l"], o=data["o"], t=data["t"], v=data["v"]
    )
    if "n" in data:
        ohlc.n = data["n"]

    if "vw" in data:
        ohlc.vw = data["vw"]

    if "otc" in data:
        ohlc.otc = True

    return ohlc
