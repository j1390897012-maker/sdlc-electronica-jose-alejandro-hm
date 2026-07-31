from datetime import datetime
from typing import Protocol

from app.models.reading import ReadingModel


class ReadingRepository(Protocol):

    def add(
        self,
        sensor_id: int,
        value: float,
        unit: str,
    ) -> ReadingModel:
        ...

    def get(self, reading_id: int) -> ReadingModel | None:
        ...

    def list_for_sensor(
    self,
    sensor_id: int,
    limit: int = 50,
    offset: int = 0,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[ReadingModel]:
        ...

    def update(
        self,
        reading_id: int,
        value: float | None = None,
        unit: str | None = None,
    ) -> ReadingModel | None:
        ...

    def delete(self, reading_id: int) -> bool:
        ...