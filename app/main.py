import asyncio
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Footer, Header, Input, Log, RichLog, Static
from utils.date_tools import default_date_str, parse_date, format_date

class ConsoleBSM(App):
  """A Textual app to check equity prices and volatilities."""
  CSS_PATH = "styles.tcss"
  BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("x", "exit_app", "Exit App")]

  def compose(self) -> ComposeResult:
    """Create child widgets for the app."""
    yield Header()
    yield Grid(
      Input(placeholder="Ticker", id="ticker", classes="box", valid_empty=False),
      Button(name="OHLC", id="ohlc", label="OHLC", classes="box"),
      Button(name="OPT", id="opt", label="OPT", classes="box"),
      Input(placeholder="Date", id="date-input", classes="box", valid_empty=False, value=default_date_str()),
      Static(classes="box"),
      Button(name="CALC", id="calc", label="CALC", classes="box"),
      Button(name="CLEAR", id="clear", label="CLEAR", classes="box"),
      RichLog(id="user-output", classes="box")
    )
    yield Footer()

  def set_ohlc_disabled(self, disabled: bool) -> None:
    ticker_input = self.query_one("#ticker")
    date_input = self.query_one("#date-input")
    ohlc_button = self.query_one("#ohlc")
    clear_button = self.query_one("#clear")
    for c in [ticker_input, date_input, ohlc_button, clear_button]:
      c.disabled = disabled


  @on(Button.Pressed, "#ohlc")
  async def handle_ohlc_click(self) -> None:
    await self.fetch_ohlc_data()


  # @on(Input.Changed, "#ticker")
  # def handle_input_changed(self, event: Input.Changed) -> None:
  #   logout = self.query_one("#log", Log)
  #   logout.write_line(f"Input changed to {event.value}")

  @on(Input.Submitted, "#ticker")
  async def handle_ticker_submitted(self) -> None:
    await self.fetch_ohlc_data()

  async def fetch_ohlc_data(self) -> None:
    self.set_ohlc_disabled(True)
    if self.has_valid_fields():
      self.log_out('Fields are valid. I am prepared to fetch')
    else:
      self.log_out('Fields are not valid. Fetcher out.')
    self.log_out('going to sleep')
    await asyncio.sleep(3)
    self.log_out('waking up')
    # self.log_out(f"Ticker has value {ticker}")
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

  def get_input_ticker(self) -> str:
    ticker_input = self.query_one("#ticker", Input)
    return ticker_input.value

  def has_valid_fields(self) -> bool:
    ticker = self.get_input_ticker()
    date = self.get_input_date()
    return len(ticker) > 0 and not date is None

  def action_toggle_dark(self) -> None:
    """An action to toggle dark mode."""
    self.dark = not self.dark

  def action_exit_app(self) -> None:
    self.exit()

if __name__ == "__main__":
    app = ConsoleBSM()
    app.run()
