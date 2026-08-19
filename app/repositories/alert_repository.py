from typing import Protocol

from app.models.alert import AlertModel


class AlertRepository(Protocol):
    """Contrato de persistencia para las alertas."""

    def add(
        self,
        sensor_id: int,
        reading_id: int,
        value: float,
        threshold: float,
    ) -> AlertModel:
        """Crea y persiste una alerta."""
        ...

    def list(self) -> list[AlertModel]:
        """Lista todas las alertas."""
        ...

    def update_status(
        self,
        alert_id: int,
        status: str,
    ) -> AlertModel | None:
        """Actualiza el estado de una alerta."""
        ...