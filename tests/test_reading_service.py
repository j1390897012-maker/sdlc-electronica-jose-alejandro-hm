import pytest

from app.repositories.fake_reading_repository import (
    FakeReadingRepository,
)
from app.repositories.fake_sensor_repository import (
    FakeSensorRepository,
)
from app.services.reading_service import ReadingService


def create_service() -> ReadingService:
    reading_repo = FakeReadingRepository()
    sensor_repo = FakeSensorRepository()

    sensor_repo.add(
        "TEMP-01",
        "temperature",
        "C",
    )

    return ReadingService(
        reading_repo,
        sensor_repo,
    )


def test_record_guarda_lectura_valida() -> None:
    service = create_service()

    reading = service.record(
        sensor_id=1,
        value=25.5,
        unit="C",
    )

    assert reading.sensor_id == 1
    assert reading.value == 25.5


def test_record_rechaza_temperatura_menor_al_cero_absoluto() -> None:
    service = create_service()

    with pytest.raises(
        ValueError,
        match="cero absoluto",
    ):
        service.record(
            sensor_id=1,
            value=-300,
            unit="C",
        )


def test_listar_por_sensor() -> None:
    reading_repo = FakeReadingRepository()
    sensor_repo = FakeSensorRepository()

    sensor_repo.add(
        "TEMP-01",
        "temperature",
        "C",
    )

    sensor_repo.add(
        "TEMP-02",
        "temperature",
        "C",
    )

    service = ReadingService(
        reading_repo,
        sensor_repo,
    )

    service.record(1, 20, "C")
    service.record(2, 30, "C")
    service.record(1, 22, "C")

    readings = service.list_for_sensor(1)

    assert len(readings) == 2


def test_update_actualiza_lectura() -> None:
    service = create_service()

    reading = service.record(
        1,
        20,
        "C",
    )

    updated = service.update(
        reading.id,
        value=25,
        unit="C",
    )

    assert updated is not None
    assert updated.value == 25
    assert updated.unit == "C"


def test_delete_elimina_lectura() -> None:
    service = create_service()

    reading = service.record(
        1,
        20,
        "C",
    )

    deleted = service.delete(
        reading.id,
    )

    assert deleted is True