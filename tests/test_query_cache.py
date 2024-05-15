from app.components.QueryCache import QueryCache

def test_create_cache():
  qc = QueryCache()
  cached = qc.cache_query('abcd', '01012001', 'foo')
  assert cached is True
  assert len(qc.tickers) == 1
  assert len(qc.queries) == 1
  assert 'abcd' in qc.queries
  assert 'abcd' in qc.tickers
  assert '01012001' in qc.queries['abcd']
  assert qc.queries['abcd']['01012001'] == 'foo'

def test_false_on_none():
  qc = QueryCache()
  cached = qc.cache_query('abcd', '020202', None)
  assert cached is False

def test_repeat_values():
  qc = QueryCache()
  cache1 = qc.cache_query('abcd', '20010101', 'foo')
  cache2 = qc.cache_query('abcd', '20010102', 'bar')
  assert cache1 is True
  assert cache2 is True
  assert len(qc.tickers) == 1
  assert len(qc.queries) == 1
  assert len(qc.queries['abcd']) == 2
  assert qc.queries['abcd']['20010101'] == 'foo'
  assert qc.queries['abcd']['20010102'] == 'bar'

def test_different_values():
  qc = QueryCache()
  cache1 = qc.cache_query('abcd', '20010101', 'foo')
  cache2 = qc.cache_query('abcd', '20010102', 'bar')
  cache3 = qc.cache_query('msft', '20210304', '200')
  assert cache1 and cache2 and cache3 is True
  assert len(qc.tickers) == 2
  assert len(qc.queries) == 2
  assert len(qc.queries['abcd']) == 2
  assert len(qc.queries['msft']) == 1
  assert qc.queries['abcd']['20010101'] == 'foo'
  assert qc.queries['abcd']['20010102'] == 'bar'
  assert qc.queries['msft']['20210304'] == '200'

def test_different_caches():
  qc1 = QueryCache()
  qc1.cache_query('abcd', '01', '10')
  qc2 = QueryCache()
  qc2.cache_query('defg', '02', 'baz')
  assert 'abcd' in qc1.tickers
  assert 'abcd' not in qc2.tickers

def test_simple_cache():
  qc = QueryCache()
  qc.cache_query('abcd', '20010101', 'hello')
  assert qc.get_cache('defg', '20010101') is None
  assert qc.get_cache('abcd', '20010102') is None
  assert qc.get_cache('abcd', '20010101') == 'hello'
