from pathlib import Path

from alert_manager import AlertManager, AlertStrategy, FileAlert


class FakeAlertStrategy(AlertStrategy):

    def __init__(self) -> None:
        self.message: str | None = None

    def send(self, message: str) -> None:
        self.message = message


def test_alert_manager_sends_alert() -> None:

    strategy = FakeAlertStrategy()
    manager = AlertManager(strategy)

    manager.alert("Temperatura crítica")

    assert strategy.message == "Temperatura crítica"

def test_file_alert_guarda_mesnaje(tmp_path: Path) -> None:
    file_path = tmp_path / "alert.log"
    

    alert = FileAlert(str(file_path))
    alert.send("Temperatura Alta")

    contenido = file_path.read_text()

    assert "Temperatura Alta" in contenido
