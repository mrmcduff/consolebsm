from datetime import datetime, timedelta
import pytz
from typing import TypedDict

FORMAT_STRINGS = ["%Y-%m-%d", "%m/%d/%Y", "%d %B, %Y", "%B %d, %Y"]
#These are American equities (for now), so all dates are in New York time.
TIME_ZONE = "America/New_York"

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
  delta = timedelta(days=1)
  return format_date(default_date - delta)

def find_start_date_str(end_date_str: str, days_back: int) -> str:
  delta = timedelta(days=days_back)
  end_date = parse_date(end_date_str)["date"]
  if end_date is None:
    return "Error parsing start date"
  else:
    return format_date(end_date - delta)

def from_millis(millis: int) -> datetime:
  seconds = millis / 1000
  tz = pytz.timezone(TIME_ZONE)
  return tz.localize(datetime.fromtimestamp(seconds))
