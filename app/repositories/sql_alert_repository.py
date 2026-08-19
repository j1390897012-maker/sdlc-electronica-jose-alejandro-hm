from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import AlertModel
from app.models.reading import ReadingModel
from app.models.sensor import SensorModel


class SQLAlertRepository:
    """Implementación de AlertRepository respaldada por una base de datos SQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        sensor_id: int,
        reading_id: int,
        value: float,
        threshold: float,
    ) -> AlertModel:
        alert = AlertModel(
            sensor_id=sensor_id,
            reading_id=reading_id,
            value=value,
            threshold=threshold,
        )

        self._session.add(alert)
        self._session.commit()
        self._session.refresh(alert)

        return alert

    def list(self) -> list[AlertModel]:
        alerts = list(
            self._session.scalars(
                select(AlertModel)
        ).all()
    )

        registered_reading_ids = {
            alert.reading_id
            for alert in alerts
    }

        statement = (
            select(ReadingModel, SensorModel)
        .join(
            SensorModel,
            ReadingModel.sensor_id == SensorModel.id,
        )
        .where(
            ReadingModel.alert_triggered.is_(True),
            SensorModel.alert_threshold.is_not(None),
        )
    )

        rows = self._session.execute(statement).all()

        historical_alerts = [
            AlertModel(
            id=reading.id,
            sensor_id=reading.sensor_id,
            reading_id=reading.id,
            value=reading.value,
            threshold=sensor.alert_threshold,
            created_at=reading.created_at,
        )
            for reading, sensor in rows
            if reading.id not in registered_reading_ids
    ]

        return alerts + historical_alerts

    def update_status(
        self,
        alert_id: int,
        status: str,
    ) -> AlertModel | None:
        alert = self._session.get(AlertModel, alert_id)

        if alert is None:
            return None

        alert.status = status
        self._session.commit()
        self._session.refresh(alert)

        return alert