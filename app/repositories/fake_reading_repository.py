from app.models.reading import ReadingModel


class FakeReadingRepository:

    def __init__(self) -> None:
        self.readings: list[ReadingModel] = []
        self.next_id = 1

    def add(
        self,
        sensor_id: str,
        value: float,
        unit: str
    ) -> ReadingModel:

        reading = ReadingModel(
            id=self.next_id,
            sensor_id=sensor_id,
            value=value,
            unit=unit
        )

        self.readings.append(reading)
        self.next_id += 1

        return reading

    def list_for_sensor(
        self,
        sensor_id: str
    ) -> list[ReadingModel]:

        return [
            reading
            for reading in self.readings
            if reading.sensor_id == sensor_id
        ]

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return next(
            (reading for reading in self.readings if reading.id == reading_id),
            None,
        )