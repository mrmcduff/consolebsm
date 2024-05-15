from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class ConsoleBSM(App):
    """A Textual app to check equity prices and volatilities."""
    CSS_PATH = "styles.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("x", "exit_app", "Exit App")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_exit_app(self) -> None:
        self.exit()

if __name__ == "__main__":
    app = ConsoleBSM()
    app.run()
