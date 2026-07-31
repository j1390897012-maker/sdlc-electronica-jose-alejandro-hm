from datetime import datetime

from app.models.reading import ReadingModel
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorRepository


class ReadingService:

    def __init__(
        self,
        repo: ReadingRepository,
        sensor_repo: SensorRepository,
    ) -> None:
        self._repo = repo
        self._sensor_repo = sensor_repo

    def _validate_reading(
        self,
        sensor_id: int,
        value: float,
        unit: str,
    ) -> None:
        sensor = self._sensor_repo.get(sensor_id)

        if sensor is None:
            raise LookupError("Sensor no encontrado")

        valid_units = {
            "temperature": {"C", "F"},
            "humidity": {"%"},
            "pressure": {"hPa"},
        }

        allowed_units = valid_units[sensor.sensor_type]

        if unit not in allowed_units:
            raise ValueError(
                f"Unidad {unit!r} no válida para "
                f"sensor de tipo {sensor.sensor_type!r}"
            )

        if sensor.sensor_type == "temperature":
            if value < -273.15:
                raise ValueError(
                    "El valor no puede estar por debajo "
                    "del cero absoluto"
                )

        elif sensor.sensor_type == "humidity":
            if not 0 <= value <= 100:
                raise ValueError(
                    "La humedad debe estar entre 0 y 100"
                )

        elif sensor.sensor_type == "pressure":
            if value < 0:
                raise ValueError(
                    "La presión no puede ser negativa"
                )

    def record(
        self,
        sensor_id: int,
        value: float,
        unit: str,
    ) -> ReadingModel:
        self._validate_reading(
            sensor_id,
            value,
            unit,
        )

        return self._repo.add(
            sensor_id,
            value,
            unit,
        )

    def get_reading(
        self,
        reading_id: int,
    ) -> ReadingModel | None:
        return self._repo.get(reading_id)

    def list_for_sensor(
        self,
        sensor_id: int,
        limit: int = 50,
        offset: int = 0,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[ReadingModel]:
        return self._repo.list_for_sensor(
            sensor_id,
            limit,
            offset,
            date_from,
            date_to,
        )

    def update(
        self,
        reading_id: int,
        value: float | None = None,
        unit: str | None = None,
    ) -> ReadingModel | None:
        reading = self._repo.get(reading_id)

        if reading is None:
            return None

        new_value = (
            value
            if value is not None
            else reading.value
        )

        new_unit = (
            unit
            if unit is not None
            else reading.unit
        )

        self._validate_reading(
            reading.sensor_id,
            new_value,
            new_unit,
        )

        return self._repo.update(
            reading_id,
            value,
            unit,
        )

    def delete(self, reading_id: int) -> bool:
        return self._repo.delete(reading_id)