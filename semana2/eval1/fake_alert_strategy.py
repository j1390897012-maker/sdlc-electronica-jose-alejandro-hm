
from alert_manager import AlertStrategy


class FakeAlertStrategy(AlertStrategy):

    def __init__(self) -> None:
        self.message: str | None = None

    def send(self, message: str) -> None:
        self.message = message