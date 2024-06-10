from rich import json
from textual.widgets import RichLog


class OutputLogger:
    text_log: RichLog
    json_log: RichLog
    error_log: RichLog

    def __init__(self, text_log: RichLog, json_log: RichLog, error_log: RichLog):
        self.text_log = text_log
        self.error_log = error_log
        self.json_log = json_log
        pass

    def log_text(self, text: str) -> None:
        self.text_log.write(text)
        pass

    def log_json(self, data: json.JSON) -> None:
        self.json_log.write(data)
        pass

    def log_error(self, text: str) -> None:
        self.error_log.write(text)
        pass
