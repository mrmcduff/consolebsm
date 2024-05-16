import asyncio
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Footer, Header, Input, Log, RichLog, Static

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
      Input(placeholder="Date", id="date-input", classes="box", valid_empty=False),
      Static(classes="box"),
      Button(name="CALC", id="calc", label="CALC", classes="box"),
      Button(name="CLEAR", id="clear", label="CLEAR", classes="box"),
      RichLog(id="user-output", classes="box")
    )
    yield Footer()

  def has_valid_fields(self) -> bool:
    ticker_input = self.query_one("#ticker")
    date_input = self.query_one("#date-input")
    return len(ticker_input.value) > 0 and len(date_input.value) > 0

  def log_out(self, something: str) -> None:
    logout = self.query_one("#user-output", RichLog)
    logout.write(something)

  def set_ohlc_disabled(self, disabled: bool) -> None:
    ticker_input = self.query_one("#ticker")
    date_input = self.query_one("#date-input")
    ohlc_button = self.query_one("#ohlc")
    clear_button = self.query_one("#clear")
    for c in [ticker_input, date_input, ohlc_button, clear_button]:
      c.disabled = disabled


  @on(Button.Pressed, "#ohlc")
  async def handle_ohlc_click(self) -> None:
    ticker_holder = self.query_one("#ticker", Input)
    self.set_ohlc_disabled(True)
    if self.has_valid_fields():
      self.log_out('Fields are valid. I am prepared to fetch')
    else:
      self.log_out('Fields are not valid. Fetcher out.')

    self.log_out('going to sleep')
    await asyncio.sleep(3)
    self.log_out('waking up')
    self.log_out(f"Ticker has value {ticker_holder.value}")
    self.set_ohlc_disabled(False)



  # @on(Input.Changed, "#ticker")
  # def handle_input_changed(self, event: Input.Changed) -> None:
  #   logout = self.query_one("#log", Log)
  #   logout.write_line(f"Input changed to {event.value}")

  # @on(Input.Submitted, "#ticker")
  # def handle_input_changed(self, event: Input.Submitted) -> None:
  #   logout = self.query_one("#log", Log)
  #   logout.write_line(f"Input submitted with {event.value}")

  # async def fetch_ohlc_data(self, ticker: str) -> None:
  #   btn = self.query_one("#fetch")
  #   logout = self.query_one("#log", Log)
  #   logout.write_line("Starting second method")
  #   logout.refresh()
  #   await asyncio.sleep(3)
  #   logout.write_line(f"ending second method {ticker}")
  #   btn.loading = False
  #   self.refresh()

  def action_toggle_dark(self) -> None:
    """An action to toggle dark mode."""
    self.dark = not self.dark

  def action_exit_app(self) -> None:
    self.exit()

if __name__ == "__main__":
    app = ConsoleBSM()
    app.run()
