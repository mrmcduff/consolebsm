import httpx
import os
from typing import Any
from rich import json
from .OutputLogger import OutputLogger
from utils.model_tools import range_ohlc_from_json
from models.RangeOhlc import RangeOhlc

polygon_key = os.getenv("POLYGON_IO_API_KEY")
polygon_base = "https://api.polygon.io"
stlouis_fed_key = os.getenv("ST_LOUIS_FED_API_KEY")


class DataFetcher:
    logger: OutputLogger

    def __init__(self, logger: OutputLogger):
        self.logger = logger
        pass

    async def fetch_range_ohlc_data(
        self, ticker: str, start_date_str: str, end_date_str: str
    ) -> RangeOhlc | None:
        unformatted_json = await self.make_range_call(
            ticker=ticker, start_date_str=start_date_str, end_date_str=end_date_str
        )
        self.logger.log_text(text="Found result")
        parsed_data = range_ohlc_from_json(unformatted_json)
        if parsed_data is None:
            self.logger.log_error(f"Could not interpret result {unformatted_json}")
            return None
        return parsed_data

    async def fetch_treasury_data(self) -> float | None:
        self.logger.log_text("Fetching treasury data")
        [start_date_str, end_date_str] = self.get_current_range()
        unformatted_json = await self.make_rfr_call(
            start_date_str=start_date_str, end_date_str=end_date_str
        )
        formatted_json = json.JSON.from_data(unformatted_json)
        if formatted_json is None:
            self.logger.log_error("Something failed at the fed")
            return
        else:
            self.logger.log_json(formatted_json)
            obsvs = unformatted_json["observations"]
            if len(obsvs) > 0:
                most_recent = obsvs[0]
                mrv = most_recent["value"]
                self.logger.log_text(f"Most recent RFR is {mrv}")
                return mrv
        self.logger.log_text("waking up")

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

    async def make_rfr_call(self, start_date_str: str, end_date_str: str) -> Any | None:
        fred_url = "https://api.stlouisfed.org/fred/series/observations"
        # endpoint = "v2/accounting/od/avg_interest_rates"
        series_id = (
            "DGS1MO"  # Series ID for the 1-month Treasury constant maturity rate
        )
        # Define the parameters for the API request
        params = {
            "series_id": series_id,
            "api_key": stlouis_fed_key,
            "observation_start": start_date_str,
            "observation_end": end_date_str,
            "file_type": "json",
            "limit": 12,
            "sort_order": "desc",  # Sort in descending order to get the latest data first
        }
        self.logger.log_text("about to create the client")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(fred_url, params=params)
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
