"""Lógica de negocio del recurso Reading.

Depende de las abstracciones ReadingRepository y SensorRepository
(Protocol), no de implementaciones concretas — permite probar con
repositorios fake en memoria, sin base de datos real (DIP).
"""

from datetime import datetime

from app.constants import VALID_UNITS
from app.models.reading import ReadingModel
from app.models.sensor import SensorModel
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorRepository
from app.services.alert_notifier import AlertNotifier, ConsoleAlertNotifier


class ReadingService:
    """Orquesta las reglas de negocio del recurso Reading."""

    def __init__(
        self,
        repo: ReadingRepository,
        sensor_repo: SensorRepository,
        notifier: AlertNotifier | None = None,
    ) -> None:
        self._repo = repo
        self._sensor_repo = sensor_repo
        self._notifier = notifier or ConsoleAlertNotifier()

    def _validate_reading(
        self,
        sensor_id: int,
        value: float,
        unit: str,
    ) -> SensorModel:
        """Valida una lectura contra su sensor: existencia, unidad y
        rango físico según el tipo (temperatura/humedad/presión).

        Esta validación vive aquí y no en Pydantic porque necesita
        consultar el sensor en la base de datos para saber su tipo.
        Devuelve el sensor para que `record` no tenga que buscarlo
        de nuevo al evaluar el umbral de alerta.
        """
        sensor = self._sensor_repo.get(sensor_id)

        if sensor is None:
            raise LookupError("Sensor no encontrado")

        allowed_units = VALID_UNITS[sensor.sensor_type]

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

        return sensor

    def _check_alert(self, sensor: SensorModel, value: float) -> bool:
        """Evalúa el umbral configurado del sensor (US-08) y notifica
        si se supera (US-07). Devuelve si se disparó la alerta, para
        que quede registrado en la lectura (`alert_triggered`).
        """
        if sensor.alert_threshold is None:
            return False

        if value <= sensor.alert_threshold:
            return False

        self._notifier.notify(
            f"Sensor {sensor.name!r} ({sensor.sensor_type}): "
            f"valor {value} superó el umbral de {sensor.alert_threshold}"
        )
        return True

    def record(
        self,
        sensor_id: int,
        value: float,
        unit: str,
    ) -> ReadingModel:
        """Registra una lectura nueva, validándola primero contra su sensor.

        Si el sensor tiene `alert_threshold` configurado (US-08) y el
        valor lo supera, notifica la alerta (US-07) y la lectura queda
        marcada con `alert_triggered=True`.
        """
        sensor = self._validate_reading(
            sensor_id,
            value,
            unit,
        )

        alert_triggered = self._check_alert(sensor, value)

        return self._repo.add(
            sensor_id,
            value,
            unit,
            alert_triggered,
        )

    def get_reading(
        self,
        reading_id: int,
    ) -> ReadingModel | None:
        """Obtiene una lectura por id, o None si no existe."""
        return self._repo.get(reading_id)

    def list_for_sensor(
        self,
        sensor_id: int,
        limit: int = 50,
        offset: int = 0,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[ReadingModel]:
        """Lista lecturas de un sensor, con paginación y filtro de fecha."""
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
        """Actualiza parcialmente una lectura, revalidándola contra su sensor.

        Nota: no recalcula `alert_triggered`. Las alertas se evalúan
        al momento de ingesta (`record`); editar una lectura ya
        guardada no reabre ni reemite una alerta retroactivamente.
        """
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
        """Elimina una lectura. Devuelve False si no existía."""
        return self._repo.delete(reading_id)