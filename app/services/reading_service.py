from datetime import datetime

from app.models.reading import ReadingModel
from app.repositories.reading_repository import ReadingRepository


class ReadingService:

    def __init__(
        self,
        repo: ReadingRepository
    ) -> None:

        self._repo = repo

    def record(
    self,
    sensor_id: int,
    value: float,
    unit: str,
) -> ReadingModel:

        if value < -273.15:
            raise ValueError(
                "Temperatura por debajo del cero absoluto"
            )

        return self._repo.add(
            sensor_id,
            value,
            unit
        )

    def get_reading(
        self,
        reading_id: int
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

        if value is not None and value < -273.15:
            raise ValueError(
                "Temperatura por debajo del cero absoluto"
            )

        return self._repo.update(
            reading_id,
            value,
            unit,
        )

    def delete(self, reading_id: int) -> bool:
        return self._repo.delete(reading_id)