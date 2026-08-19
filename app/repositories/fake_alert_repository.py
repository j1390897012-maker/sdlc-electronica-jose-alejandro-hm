from app.models.alert import AlertModel


class FakeAlertRepository:
    """Repositorio en memoria para pruebas de alertas."""

    def __init__(self) -> None:
        self.alerts: list[AlertModel] = []

    def add(
        self,
        sensor_id: int,
        reading_id: int,
        value: float,
        threshold: float,
    ) -> AlertModel:
        alert = AlertModel(
            id=len(self.alerts) + 1,
            sensor_id=sensor_id,
            reading_id=reading_id,
            value=value,
            threshold=threshold,
        )

        self.alerts.append(alert)

        return alert

    def list(self) -> list[AlertModel]:
        return list(self.alerts)

    def update_status(
        self,
        alert_id: int,
        status: str,
    ) -> AlertModel | None:
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.status = status
                return alert

        return None