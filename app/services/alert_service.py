from app.models.alert import AlertModel
from app.repositories.alert_repository import AlertRepository

VALID_STATUSES = {
    "open",
    "acknowledged",
    "resolved",
}


class AlertService:
    """Orquesta las operaciones de consulta y registro de alertas."""

    def __init__(self, repo: AlertRepository) -> None:
        self._repo = repo

    def create(
        self,
        sensor_id: int,
        reading_id: int,
        value: float,
        threshold: float,
    ) -> AlertModel:
        """Registra una alerta generada por una lectura."""
        return self._repo.add(
            sensor_id,
            reading_id,
            value,
            threshold,
        )

    def list(self) -> list[AlertModel]:
        """Lista las alertas registradas."""
        return self._repo.list()

    def update_status(
        self,
        alert_id: int,
        status: str,
    ) -> AlertModel | None:
        """Actualiza el estado de una alerta."""
        if status not in VALID_STATUSES:
            raise ValueError(f"Estado inválido: {status!r}")

        return self._repo.update_status(alert_id, status)