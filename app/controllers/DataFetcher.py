import httpx
import os
from typing import Any
from .OutputLogger import OutputLogger
from utils.model_tools import range_ohlc_from_json
from models.RangeOhlc import RangeOhlc

polygon_key = os.getenv("POLYGON_IO_API_KEY")
polygon_base = "https://api.polygon.io"
stlouis_fed_key = os.getenv("ST_LOUIS_FED_API_KEY")


class DataFetcher:
    logger: OutputLogger

    def __init__(self, logger: OutputLogger):
        self.logger = OutputLogger
        pass

    async def fetch_range_ohlc_data(
        self, ticker: str, start_date_str: str, end_date_str: str
    ) -> RangeOhlc | None:
        unformatted_json = await self.make_range_call(
            ticker=ticker, start_date_str=start_date_str, end_date_str=end_date_str
        )
        self.logger.log_text("Found result")
        parsed_data = range_ohlc_from_json(unformatted_json)
        if parsed_data is None:
            self.logger.log_error(f"Could not interpret result {unformatted_json}")
            return None
        return parsed_data

    async def make_range_call(
        self,
        ticker: str,
        start_date_str: str,
        end_date_str: str,
    ) -> Any | None:
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker.upper()}/range/1/day/{start_date_str}/{end_date_str}?adjusted=true&sort=asc"
        headers = {"Authorization": f"Bearer {polygon_key}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors
                return response.json()
            except httpx.RequestError as exc:
                self.logger.log_error(
                    f"An error occurred while requesting {exc.request.url!r}."
                )
            except httpx.HTTPStatusError as exc:
                self.logger.log_error(
                    f"Error response {exc.response.reason_phrase} while requesting {exc.request.url!r}."
                )
            except Exception as exc:
                self.logger.log_error(f"An unexpected error occurred: {exc}")
