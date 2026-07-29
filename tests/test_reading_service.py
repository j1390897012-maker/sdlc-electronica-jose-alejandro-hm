import pytest

from app.repositories.fake_reading_repository import (
    FakeReadingRepository,
)
from app.services.reading_service import ReadingService


def test_record_guarda_lectura_valida() -> None:

    repo = FakeReadingRepository()
    service = ReadingService(repo)

    reading = service.record(
        sensor_id="TEMP-01",
        value=25.5,
        unit="C",
    )

    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 25.5
    assert len(repo.readings) == 1


def test_record_rechaza_temperatura_menor_al_cero_absoluto() -> None:

    repo = FakeReadingRepository()
    service = ReadingService(repo)

    with pytest.raises(ValueError):
        service.record(
            sensor_id="TEMP-01",
            value=-300,
            unit="C",
        )


def test_listar_por_sensor() -> None:

    repo = FakeReadingRepository()
    service = ReadingService(repo)

    service.record("TEMP-01", 20, "C")
    service.record("TEMP-02", 30, "C")
    service.record("TEMP-01", 22, "C")

    readings = repo.list_for_sensor("TEMP-01")

    assert len(readings) == 2