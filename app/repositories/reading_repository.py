"""Contrato de acceso a datos para el recurso Reading.

Implementado por SQLReadingRepository (producción) y
FakeReadingRepository (tests, en memoria). ReadingService depende
de este Protocol, no de una implementación concreta (DIP).
"""

from datetime import datetime
from typing import Protocol

from app.models.reading import ReadingModel


class ReadingRepository(Protocol):
    """Operaciones de persistencia que debe ofrecer un repositorio de lecturas."""

    def add(
        self,
        sensor_id: int,
        value: float,
        unit: str,
        alert_triggered: bool = False,
    ) -> ReadingModel:
        """Crea y persiste una lectura nueva."""
        ...

    def get(self, reading_id: int) -> ReadingModel | None:
        """Busca una lectura por id."""
        ...

    def list_for_sensor(
    self,
    sensor_id: int,
    limit: int = 50,
    offset: int = 0,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[ReadingModel]:
        """Lista las lecturas de un sensor, con paginación y filtro de fecha."""
    ...

    def list_stats_for_sensor(
        self,
        sensor_id: int,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[ReadingModel]:
        """Calcula estadísticas (min, max, avg) de las lecturas de un sensor."""
        ...


    def update(
        self,
        reading_id: int,
        value: float | None = None,
        unit: str | None = None,
    ) -> ReadingModel | None:
        """Actualiza los campos provistos de una lectura existente."""
        ...

    def delete(self, reading_id: int) -> bool:
        """Elimina una lectura por id."""
        ...