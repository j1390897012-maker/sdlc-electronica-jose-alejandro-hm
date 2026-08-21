"""Implementación en memoria de ReadingRepository, solo para tests."""

from datetime import datetime

from app.models.reading import ReadingModel


class FakeReadingRepository:
    """Doble de prueba de ReadingRepository: guarda todo en una lista en memoria.

    Permite probar ReadingService sin base de datos real (ver
    tests/test_reading_service.py), pagando el DIP aplicado en el servicio.
    """

    def __init__(self) -> None:
        self.readings: list[ReadingModel] = []
        self.next_id = 1

    def add(
        self,
        sensor_id: int,
        value: float,
        unit: str,
        alert_triggered: bool = False,
    ) -> ReadingModel:
        reading = ReadingModel(
            id=self.next_id,
            sensor_id=sensor_id,
            value=value,
            unit=unit,
            alert_triggered=alert_triggered,
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


    def list_stats_for_sensor(
        self,
        sensor_id: int,
        date_from: datetime | None = None, 
        date_to: datetime | None = None,
    ) -> list[ReadingModel]:
        """Calcula estadísticas (min, max, avg) de las lecturas de un sensor."""   
        
        readings = [
            reading
            for reading in self.readings
            if reading.sensor_id == sensor_id
        ]

        if date_from is not None:
            readings = [
                reading for reading in 
                readings if reading.created_at  >= date_from
                ]


        if date_to is not None:
            readings = [
                reading for reading in 
                readings if reading.created_at <= date_to
                ]   
        return readings





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