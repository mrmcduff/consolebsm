from datetime import datetime
from typing import TypedDict, Optional

FORMAT_STRINGS = ["%Y-%m-%d", "%m/%d/%Y", "%d %B, %Y", "%B %d, %Y"]

Date_Response = TypedDict('Date_Response', { 'valid': bool, 'date': datetime | None, 'error': str | None })

def parse_date(possible_date: str) -> Date_Response:
  response = None

  for f in FORMAT_STRINGS:
    try:
      response = datetime.strptime(possible_date, f)
      return {'valid': True, 'date': response, 'error': None }
    except ValueError as ve:
      # failed this way, will move on.
      continue

  return {'valid': False, 'date': response, 'error': f"{possible_date} could not be parsed as a date" }

def format_date(query_date: datetime) -> str:
  return datetime.strftime(query_date, FORMAT_STRINGS[0])

def default_date_str(default_date: datetime = datetime.now()) -> str:
  return format_date(default_date)
