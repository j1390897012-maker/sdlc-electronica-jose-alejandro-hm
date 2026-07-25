from alert_manager import AlertStrategy
from typing import Optional


class FakeAlertStrategy(AlertStrategy):

    def __init__(self) -> None:
        self.message: Optional[str] = None

    def send(self, message: str) -> None:
        self.message = message