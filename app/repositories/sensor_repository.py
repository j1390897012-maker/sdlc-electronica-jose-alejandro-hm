"""Contrato de acceso a datos para el recurso Sensor.

Implementado por SQLSensorRepository (producción, ver
sql_sensor_repository.py) y FakeSensorRepository (tests, en memoria).
SensorService depende de este Protocol, no de una implementación
concreta — eso es lo que permite el DIP.
"""

from typing import Protocol

from app.models.sensor import SensorModel


class SensorRepository(Protocol):
    """Operaciones de persistencia que debe ofrecer un repositorio de sensores."""

    def add(
        self,
        name: str,
        sensor_type: str,
        unit: str,
        alert_threshold: float | None = None,
    ) -> SensorModel:
        """Crea y persiste un sensor nuevo."""
        ...

    def get(self, sensor_id: int) -> SensorModel | None:
        """Busca un sensor por id."""
        ...

    def get_by_name(self, name: str) -> SensorModel | None:
        """Busca un sensor por nombre (clave de negocio única)."""
        ...

    def list(self) -> list[SensorModel]:
        """Lista todos los sensores."""
        ...

    def update(
        self,
        sensor_id: int,
        name: str | None = None,
        sensor_type: str | None = None,
        unit: str | None = None,
        alert_threshold: float | None = None,
    ) -> SensorModel | None:
        """Actualiza los campos provistos de un sensor existente."""
        ...

    def delete(self, sensor_id: int) -> bool:
        """Elimina un sensor por id."""
        ...