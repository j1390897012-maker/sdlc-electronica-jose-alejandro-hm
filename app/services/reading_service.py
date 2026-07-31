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
        sensor_id: str,
        value: float,
        unit: str
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

        return self._repo.get_by_id(reading_id)