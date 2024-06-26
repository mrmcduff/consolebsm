import httpx
import os
from typing import Any, Tuple
from textual import on
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.containers import Grid
from textual.widgets import Button, Footer, Header, Input, RichLog, Static
from controllers.DataFetcher import DataFetcher
from controllers.OutputLogger import OutputLogger
from utils.date_tools import (
    default_date_str,
    parse_date,
    format_date,
    find_start_date_str,
    from_millis,
)
from dotenv import load_dotenv
from rich import json
from utils.format_tools import get_closes
from utils.model_tools import get_range_values
from utils.volatility_tools import calculate_volatility, calculate_daily_volatility

load_dotenv()
polygon_key = os.getenv("POLYGON_IO_API_KEY")
polygon_base = "https://api.polygon.io"
stlouis_fed_key = os.getenv("ST_LOUIS_FED_API_KEY")


class ConsoleBSM(App):
    """A Textual app to check equity prices and volatilities."""

    CSS_PATH = "styles.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("x", "exit_app", "Exit App")]

    span_count: reactive[int] = reactive(1)
    output_controller: OutputLogger
    data_fetcher: DataFetcher
    output_log_view: RichLog

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # here, do self.richlog = ...
        # then yield self.richlog
        self.output_log_view = RichLog(
            id="user-output", classes="box bordered full tall", wrap=True
        )
        self.output_controller = OutputLogger(
            text_log=self.output_log_view,
            json_log=self.output_log_view,
            error_log=self.output_log_view,
        )
        self.data_fetcher = DataFetcher(self.output_controller)
        # For now, just use the same output view for all logs.

        yield Header()
        yield Grid(
            Input(
                placeholder="Ticker",
                id="ticker",
                classes="box bordered double",
                valid_empty=False,
            ),
            Button(name="OHLC", id="ohlc", label="OHLC", classes="box bordered double"),
            Button(name="OPT", id="opt", label="OPT", classes="box bordered double"),
            Button(
                name="TREAS",
                id="treasury",
                label="TREAS",
                classes="box bordered double",
            ),
            Button(
                name="CLEAR",
                id="clear",
                label="CLEAR",
                classes="box bordered quadruple",
            ),
            Input(
                placeholder="Date",
                id="date-input",
                classes="box bordered double",
                valid_empty=False,
                value=default_date_str(),
            ),
            Static(f"{self.span_count}", id="span", classes="box bordered centertext"),
            Button(
                name="PLUS",
                label="+",
                id="plus_button",
                classes="box bordered centertext",
            ),
            Button(
                name="MINUS",
                label="-",
                id="minus_button",
                classes="box bordered centertext",
            ),
            Static(classes="sevenfold"),
            self.output_log_view,
        )
        yield Footer()

    def set_ohlc_disabled(self, disabled: bool) -> None:
        ticker_input = self.query_one("#ticker")
        date_input = self.query_one("#date-input")
        ohlc_button = self.query_one("#ohlc")
        clear_button = self.query_one("#clear")
        for c in [ticker_input, date_input, ohlc_button, clear_button]:
            c.disabled = disabled

    @on(Button.Pressed, "#plus_button")
    def add_span(self) -> None:
        # TODO account for max
        span_display = self.query_one("#span", Static)
        self.span_count = self.span_count + 1
        span_display.update(f"{self.span_count}")

    @on(Button.Pressed, "#minus_button")
    def subtract_span(self) -> None:
        span_display = self.query_one("#span", Static)
        if self.span_count > 1:
            self.span_count = self.span_count - 1
            span_display.update(f"{self.span_count}")

    @on(Button.Pressed, "#ohlc")
    async def handle_ohlc_click(self) -> None:
        await self.get_ohlc_range_data()

    @on(Button.Pressed, "#treasury")
    async def handle_treasury_click(self) -> None:
        await self.fetch_treasury_data()

    @on(Input.Submitted, "#ticker")
    async def handle_ticker_submitted(self) -> None:
        await self.get_ohlc_range_data()

    async def fetch_treasury_data(self) -> float | None:
        self.output_controller.log_text("Fetching treasury data")
        [start_date_str, end_date_str] = self.get_current_range()
        unformatted_json = await self.make_rfr_call(
            start_date_str=start_date_str, end_date_str=end_date_str
        )
        formatted_json = json.JSON.from_data(unformatted_json)
        if formatted_json is None:
            self.output_controller.log_error("Something failed at the fed")
            return
        else:
            self.output_controller.log_json(formatted_json)
            obsvs = unformatted_json["observations"]
            if len(obsvs) > 0:
                most_recent = obsvs[0]
                mrv = most_recent["value"]
                self.output_controller.log_text(f"Most recent RFR is {mrv}")
                return mrv
        self.output_controller.log_text("waking up")
        # self.set_ohlc_disabled(False)

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
        self.output_controller.log_text("about to create the client")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(fred_url, params=params)
                response.raise_for_status()  # Raise an exception for HTTP errors
                return response.json()
            except httpx.RequestError as exc:
                self.output_controller.log_error(
                    f"An error occurred while requesting {exc.request.url!r}."
                )
            except httpx.HTTPStatusError as exc:
                self.output_controller.log_error(
                    f"Error response {exc.response.reason_phrase} while requesting {exc.request.url!r}."
                )
            except Exception as exc:
                self.output_controller.log_error(f"An unexpected error occurred: {exc}")

    async def get_ohlc_range_data(self) -> None:
        if self.has_valid_fields():
            self.output_controller.log_text("Fields valid. Fetching ranged data")
        else:
            self.output_controller.log_text("Invalid fields. Stopping")
            return
        ticker = self.get_input_ticker()
        [start_date_str, end_date_str] = self.get_current_range()
        range_data = await self.data_fetcher.fetch_range_ohlc_data(
            ticker=ticker, start_date_str=start_date_str, end_date_str=end_date_str
        )
        if range_data is None:
            self.output_controller.log_error("Error getting OHLC data")
        else:
            closes = get_range_values(rangeOhlc=range_data, key="c")
            raw_dates = get_range_values(rangeOhlc=range_data, key="t")
            dates = [*map(lambda t: format_date(from_millis(t)), raw_dates)]
            [sigma_hat_c, error_c] = calculate_volatility(closes)
            self.output_controller.log_text(f"Data for {ticker.upper()}")
            self.output_controller.log_text(
                f"Volatility for {len(closes)}-day period ending {end_date_str} is {sigma_hat_c}"
            )
            self.output_controller.log_text(f"Error for range is {error_c}")
            self.output_controller.log_json(str(closes))
            self.output_controller.log_json(str(dates))

        self.output_controller.log_text("waking up")
        self.set_ohlc_disabled(False)

    def get_input_date(self) -> str | None:
        date_input = self.query_one("#date-input", Input)
        date_response = parse_date(date_input.value)
        if date_response["valid"]:
            return format_date(date_response["date"])
        self.log_out(f"Invalid date error: {date_response['error']}")
        return None

    def log_out(self, something: str) -> None:
        logout = self.query_one("#user-output", RichLog)
        logout.write(something)

    def log_json(self, data: json.JSON) -> None:
        logout = self.query_one("#user-output", RichLog)
        logout.write(data)

    def get_input_ticker(self) -> str:
        ticker_input = self.query_one("#ticker", Input)
        return ticker_input.value

    def get_current_range(self) -> Tuple[str, str]:
        end_date_str = self.get_input_date()
        days_back = self.span_count
        start_date_str = find_start_date_str(
            end_date_str=end_date_str, days_back=days_back
        )
        return [start_date_str, end_date_str]

    def has_valid_fields(self) -> bool:
        ticker = self.get_input_ticker()
        date = self.get_input_date()
        return len(ticker) > 0 and date is not None

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_exit_app(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = ConsoleBSM()
    app.run()
