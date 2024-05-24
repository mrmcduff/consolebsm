import httpx
import os
from typing import Any
from .OutputLogger import OutputLogger

polygon_key = os.getenv("POLYGON_IO_API_KEY")
polygon_base = "https://api.polygon.io"
stlouis_fed_key = os.getenv("ST_LOUIS_FED_API_KEY")


class DataFetcher:
    def __init__(self):
        pass

    async def fetch_range_ohlc_data(
        self,
        ticker: str,
        start_date_str: str,
        end_date_str: str,
        logger: OutputLogger,
    ):
        unformatted_json = await self.make_range_call(
            ticker=ticker, start_date_str=start_date_str, end_date_str=end_date_str
        )
        logger.log_text('Found result')
        return unformatted_json

    async def make_range_call(
        self,
        ticker: str,
        start_date_str: str,
        end_date_str: str,
        logger: OutputLogger,
    ) -> Any | None:
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker.upper()}/range/1/day/{start_date_str}/{end_date_str}?adjusted=true&sort=asc"
        headers = {"Authorization": f"Bearer {polygon_key}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors
                return response.json()
            except httpx.RequestError as exc:
                logger.log_error(
                    f"An error occurred while requesting {exc.request.url!r}."
                )
            except httpx.HTTPStatusError as exc:
                logger.log_error(
                    f"Error response {exc.response.reason_phrase} while requesting {exc.request.url!r}."
                )
            except Exception as exc:
                logger.log_error(f"An unexpected error occurred: {exc}")