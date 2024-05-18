from textual import on
from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Log, RichLog, Static, Digits


class CounterButton(Static):

  def compose(self) -> ComposeResult:
    with Horizontal(classes="box"):
      with Vertical(classes="vertical"):
        yield Digits(value="1", id="days_display", classes="combodigit")
      with Horizontal(classes="wrapper"):
        yield Button(label="+", name="plus_button", id="plus_button")
        yield Button(label="-", name="minus_button", id="minus_button")
