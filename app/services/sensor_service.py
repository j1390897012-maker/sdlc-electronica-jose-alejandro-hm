"""Lógica de negocio del recurso Sensor.

Depende de la abstracción SensorRepository (Protocol), no de una
implementación concreta — así se puede probar con FakeSensorRepository
sin tocar base de datos (DIP, ver tests/test_sensor_service.py).
"""

from app.constants import VALID_UNITS
from app.models.sensor import SensorModel
from app.repositories.sensor_repository import SensorRepository


class SensorDuplicadoError(Exception):
    """Se lanza al intentar crear un sensor con un nombre ya existente.

    El router la traduce a HTTP 409 Conflict.
    """

    pass


class SensorService:
    """Orquesta las reglas de negocio del recurso Sensor."""

    def __init__(self, repo: SensorRepository) -> None:
        self._repo = repo

    def create(
        self,
        name: str,
        sensor_type: str,
        unit: str,
    ) -> SensorModel:
        """Crea un sensor nuevo, validando que el nombre no esté en uso."""

        if self._repo.get_by_name(name) is not None:
            raise SensorDuplicadoError(
                f"Ya existe un sensor con nombre {name!r}"
            )

        return self._repo.add(
            name,
            sensor_type,
            unit,
        )

    def get(self, sensor_id: int) -> SensorModel | None:
        """Obtiene un sensor por id, o None si no existe."""
        return self._repo.get(sensor_id)

    def list(self) -> list[SensorModel]:
        """Lista todos los sensores registrados."""
        return self._repo.list()

    def update(
        self,
        sensor_id: int,
        name: str | None = None,
        sensor_type: str | None = None,
        unit: str | None = None,
    ) -> SensorModel | None:
        """Actualiza parcialmente un sensor.

        Revalida la combinación tipo/unidad resultante (considerando
        los valores actuales para los campos que no vienen en el patch),
        para no dejar un sensor en un estado físicamente inválido.
        """

        sensor = self._repo.get(sensor_id)

        if sensor is None:
            return None

        new_sensor_type = (
            sensor_type
            if sensor_type is not None
            else sensor.sensor_type
        )

        new_unit = (
            unit
            if unit is not None
            else sensor.unit
        )

        if new_unit not in VALID_UNITS[new_sensor_type]:
            raise ValueError(
                f"Unidad {new_unit!r} no válida para "
                f"{new_sensor_type!r}"
            )

        return self._repo.update(
            sensor_id,
            name,
            sensor_type,
            unit,
        )

    def delete(self, sensor_id: int) -> bool:
        """Elimina un sensor. Devuelve False si no existía."""
        return self._repo.delete(sensor_id)