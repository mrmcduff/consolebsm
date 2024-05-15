from typing import Optional

class QueryCache:

  tickers = set()
  queries = {}

  def __init__(self):
    self.tickers = set()
    self.queries = {}
    pass

  def cache_query(self, ticker: str, date: str, data: any) -> bool:
    if data is None:
      return False

    if ticker not in self.tickers:
      self.tickers.add(ticker)
      self.queries[ticker] = {}

    self.queries[ticker][date] = data
    return True

  def get_cache(self, ticker: str, date: str) -> Optional[any]:
    if ticker not in self.tickers:
      return None
    ticker_values = self.queries[ticker]
    if date in ticker_values:
      return ticker_values[date]
    else:
      return None

  def dump_tickers(self):
    return str(self.tickers)

  def dump_queries(self):
    return str(self.queries)
