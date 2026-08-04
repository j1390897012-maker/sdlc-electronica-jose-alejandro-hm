"""Implementación real de ReadingRepository sobre SQLAlchemy."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reading import ReadingModel


class SQLReadingRepository:
    """Implementación de ReadingRepository respaldada por una base de datos SQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        sensor_id: int,
        value: float,
        unit: str,
        alert_triggered: bool = False,
    ) -> ReadingModel:
        reading = ReadingModel(
            sensor_id=sensor_id,
            value=value,
            unit=unit,
            alert_triggered=alert_triggered,
        )

        self._session.add(reading)
        self._session.commit()
        self._session.refresh(reading)

        return reading

    def get(self, reading_id: int) -> ReadingModel | None:
        return self._session.get(ReadingModel, reading_id)

    def list_for_sensor(
        self,
        sensor_id: int,
        limit: int = 50,
        offset: int = 0,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[ReadingModel]:
        statement = (
            select(ReadingModel)
            .where(ReadingModel.sensor_id == sensor_id)
        )

        if date_from is not None:
            statement = statement.where(
                ReadingModel.created_at >= date_from
            )

        if date_to is not None:
            statement = statement.where(
                ReadingModel.created_at <= date_to
            )

        statement = (
            statement
            .offset(offset)
            .limit(limit)
        )

        return list(
            self._session.scalars(statement).all()
        )

    def update(
        self,
        reading_id: int,
        value: float | None = None,
        unit: str | None = None,
    ) -> ReadingModel | None:
        reading = self.get(reading_id)

        if reading is None:
            return None

        if value is not None:
            reading.value = value

        if unit is not None:
            reading.unit = unit

        self._session.commit()
        self._session.refresh(reading)

        return reading

    def delete(self, reading_id: int) -> bool:
        reading = self.get(reading_id)

        if reading is None:
            return False

        self._session.delete(reading)
        self._session.commit()

        return True