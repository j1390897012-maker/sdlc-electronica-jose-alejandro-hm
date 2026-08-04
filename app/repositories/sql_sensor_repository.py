"""Implementación real de SensorRepository sobre SQLAlchemy."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor import SensorModel


class SQLSensorRepository:
    """Implementación de SensorRepository respaldada por una base de datos SQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        name: str,
        sensor_type: str,
        unit: str,
        alert_threshold: float | None = None,
    ) -> SensorModel:

        sensor = SensorModel(
            name=name,
            sensor_type=sensor_type,
            unit=unit,
            alert_threshold=alert_threshold,
        )

        self._session.add(sensor)
        self._session.commit()
        self._session.refresh(sensor)

        return sensor

    def get(self, sensor_id: int) -> SensorModel | None:
        return self._session.get(
            SensorModel,
            sensor_id,
        )


    def get_by_name(self, name: str) -> SensorModel | None:
        statement = select(SensorModel).where(
            SensorModel.name == name
    )

        return self._session.scalars(statement).first()




    def list(self) -> list[SensorModel]:
        statement = select(SensorModel)

        return list(
            self._session.scalars(statement).all()
        )

    def update(
        self,
        sensor_id: int,
        name: str | None = None,
        sensor_type: str | None = None,
        unit: str | None = None,
        alert_threshold: float | None = None,
    ) -> SensorModel | None:

        sensor = self.get(sensor_id)

        if sensor is None:
            return None

        if name is not None:
            sensor.name = name

        if sensor_type is not None:
            sensor.sensor_type = sensor_type

        if unit is not None:
            sensor.unit = unit

        if alert_threshold is not None:
            sensor.alert_threshold = alert_threshold

        self._session.commit()
        self._session.refresh(sensor)

        return sensor

    def delete(self, sensor_id: int) -> bool:

        sensor = self.get(sensor_id)

        if sensor is None:
            return False

        self._session.delete(sensor)
        self._session.commit()

        return True