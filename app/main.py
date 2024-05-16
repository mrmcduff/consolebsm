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
      Input(placeholder="Ticker", id="ticker", classes="box"),
      Button(name="OHLC", id="ohlc", label="OHLC", classes="box"),
      Button(name="OPT", id="opt", label="OPT", classes="box"),
      Input(placeholder="Date", id="date-input", classes="box"),
      Static(classes="box"),
      Button(name="CALC", id="calc", label="CALC", classes="box"),
      Button(name="CLEAR", id="clear", label="CLEAR", classes="box"),
      RichLog(id="user-output", classes="box")
    )
    yield Footer()

  @on(Button.Pressed, "#fetch")
  async def handle_button_click(self) -> None:
    logout = self.query_one("#log", Log)
    btn = self.query_one("#fetch")
    btn.loading = True
    text_holder = self.query_one("#ticker", Input)
    logout.write_line("Starting task")
    self.log_out('going to sleep')
    await asyncio.sleep(3)
    self.log_out('waking up')

    await self.fetch_ohlc_data("hello")
    logout.write_line("Task complete")
    btn.loading = False
    logout.write_line(f"Button was pressed: {text_holder.value}")

  def log_out(self, something: str) -> None:
    logout = self.query_one("#log", Log)
    logout.write_line(something)


  @on(Input.Changed, "#ticker")
  def handle_input_changed(self, event: Input.Changed) -> None:
    logout = self.query_one("#log", Log)
    logout.write_line(f"Input changed to {event.value}")

  @on(Input.Submitted, "#ticker")
  def handle_input_changed(self, event: Input.Submitted) -> None:
    logout = self.query_one("#log", Log)
    logout.write_line(f"Input submitted with {event.value}")

  async def fetch_ohlc_data(self, ticker: str) -> None:
    btn = self.query_one("#fetch")
    logout = self.query_one("#log", Log)
    logout.write_line("Starting second method")
    logout.refresh()
    await asyncio.sleep(3)
    logout.write_line(f"ending second method {ticker}")
    btn.loading = False
    self.refresh()

  def action_toggle_dark(self) -> None:
    """An action to toggle dark mode."""
    self.dark = not self.dark

  def action_exit_app(self) -> None:
    self.exit()

if __name__ == "__main__":
    app = ConsoleBSM()
    app.run()
