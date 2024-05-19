from textual import on
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Input


class InputStack(Widget):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Ticker", id="ticker_input", valid_empty=False)
        yield Input(placeholder="Date", id="date_input", valid_empty=False)

    @on(Input.Submitted, "#ticker_input")
    def handle_input_submitted(self, event: Input.Submitted) -> None:
        # ticker = self.query_one("#ticker_input", Input)
        date_input = self.query_one("#date_input", Input)
        if date_input.value == "":
            date_input.focus()
        elif not date_input.is_valid:
            # send a message that can be passed to the logger
            pass
        else:
            # simulate sending a message to the server
            pass
