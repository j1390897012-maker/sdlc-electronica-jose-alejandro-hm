from datetime import datetime

from app.models.reading import ReadingModel


class FakeReadingRepository:

    def __init__(self) -> None:
        self.readings: list[ReadingModel] = []
        self.next_id = 1

    def add(
        self,
        sensor_id: int,
        value: float,
        unit: str,
    ) -> ReadingModel:
        reading = ReadingModel(
            id=self.next_id,
            sensor_id=sensor_id,
            value=value,
            unit=unit,
        )

        self.readings.append(reading)
        self.next_id += 1

        return reading

    def get(
        self,
        reading_id: int,
    ) -> ReadingModel | None:
        return next(
            (
                reading
                for reading in self.readings
                if reading.id == reading_id
            ),
            None,
        )

    def list_for_sensor(
        self,
        sensor_id: int,
        limit: int = 50,
        offset: int = 0,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[ReadingModel]:
        readings = [
            reading
            for reading in self.readings
            if reading.sensor_id == sensor_id
        ]

        return readings[offset : offset + limit]

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

        return reading

    def delete(
        self,
        reading_id: int,
    ) -> bool:
        reading = self.get(reading_id)

        if reading is None:
            return False

        self.readings.remove(reading)

        return True