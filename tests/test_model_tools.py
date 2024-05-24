from app.utils.model_tools import ohlc_result_from_json, range_ohlc_from_json

sample_result = {
    "c": 74.3575,
    "h": 75.145,
    "l": 74.125,
    "n": 1,
    "o": 74.2875,
    "t": 1578027600000,
    "v": 146535512,
    "vw": 74.7026,
}

sample_range = {
    "adjusted": True,
    "next_url": "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/1578114000000/2020-01-10?cursor=bGltaXQ9MiZzb3J0PWFzYw",
    "queryCount": 2,
    "request_id": "6a7e466379af0a71039d60cc78e72282",
    "results": [
        {
            "c": 75.0875,
            "h": 75.15,
            "l": 73.7975,
            "n": 1,
            "o": 74.06,
            "t": 1577941200000,
            "v": 135647456,
            "vw": 74.6099,
        },
        {
            "c": 74.3575,
            "h": 75.145,
            "l": 74.125,
            "n": 1,
            "o": 74.2875,
            "t": 1578027600000,
            "v": 146535512,
            "vw": 74.7026,
        },
    ],
    "resultsCount": 2,
    "status": "OK",
    "ticker": "AAPL",
}


def test_range_result_parse():
    ohlc_result = ohlc_result_from_json(sample_result)
    assert ohlc_result.o == sample_result["o"]
    assert ohlc_result.h == sample_result["h"]
    assert ohlc_result.l == sample_result["l"]
    assert ohlc_result.c == sample_result["c"]
    assert ohlc_result.n == sample_result["n"]
    assert ohlc_result.o == sample_result["o"]
    assert ohlc_result.t == sample_result["t"]
    assert ohlc_result.v == sample_result["v"]
    assert ohlc_result.vw == sample_result["vw"]
    assert ohlc_result.otc is False


def test_range_parse():
    range_result = range_ohlc_from_json(sample_range)
    assert range_result.adjusted == sample_range["adjusted"]
    assert range_result.ticker == sample_range["ticker"]
    assert range_result.next_url == sample_range["next_url"]
    assert range_result.resultsCount == sample_range["resultsCount"]
    assert range_result.queryCount == sample_range["queryCount"]
    assert range_result.status == sample_range["status"]
    assert range_result.request_id == sample_range["request_id"]
    assert len(range_result.results) == 2
    expected_item = ohlc_result_from_json(sample_result)
    found_items = [r for r in range_result.results if r.t == expected_item.t]
    assert len(found_items) == 1
    assert found_items[0] == expected_item
