from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Footer, Header, Input, Log, RichLog, Static


class ConsoleBSM(App):
    """A Textual app to check equity prices and volatilities."""
    CSS_PATH = "styles.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("x", "exit_app", "Exit App")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Horizontal(
          Input(placeholder="Ticker", id="ticker", classes="input"),
          Button(label="Fetch OHLC", id="fetch", classes="button"),
        )
        yield RichLog(classes="vspacer")
        yield Log(max_lines=2, id="keylog", classes="keylog", auto_scroll=True)
        yield Log(max_lines=2, id="log", classes="log", auto_scroll=True)
        yield Footer()

    @on(Button.Pressed, "#fetch")
    def handle_button_click(self) -> None:
        logout = self.query_one("#log", Log)
        text_holder = self.query_one("#ticker", Input)
        logout.write_line(f"Button was pressed: {text_holder.value}")

    @on(Input.Changed, "#ticker")
    def handle_input_changed(self, event: Input.Changed) -> None:
        logout = self.query_one("#log", Log)
        logout.write_line(f"Input changed to {event.value}")

    @on(Input.Submitted, "#ticker")
    def handle_input_changed(self, event: Input.Submitted) -> None:
        logout = self.query_one("#log", Log)
        logout.write_line(f"Input submitted with {event.value}")

    def on_key(self, event: events.Key ) -> None:
        logout = self.query_one("#keylog", Log)
        logout.write(event.character)


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_exit_app(self) -> None:
        self.exit()

if __name__ == "__main__":
    app = ConsoleBSM()
    app.run()
