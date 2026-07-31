import pytest

from app.repositories.fake_reading_repository import (
    FakeReadingRepository,
)
from app.services.reading_service import ReadingService


def test_record_guarda_lectura_valida() -> None:

    repo = FakeReadingRepository()
    service = ReadingService(repo)

    reading = service.record(
        sensor_id=1,
        value=25.5,
        unit="C",
    )

    assert reading.sensor_id == 1
    assert reading.value == 25.5
    assert len(repo.readings) == 1


def test_record_rechaza_temperatura_menor_al_cero_absoluto() -> None:

    repo = FakeReadingRepository()
    service = ReadingService(repo)

    with pytest.raises(ValueError):
        service.record(
            sensor_id= 1 ,
            value=-300,
            unit="C",
        )


def test_listar_por_sensor() -> None:

    repo = FakeReadingRepository()
    service = ReadingService(repo)

    service.record( 1, 20, "C")
    service.record( 2, 30, "C")
    service.record( 1, 22, "C")

    readings = repo.list_for_sensor( 1 )

    assert len(readings) == 2


def test_update_actualiza_lectura() -> None:

    repo = FakeReadingRepository()
    service = ReadingService(repo)

    reading = service.record(1, 20, "C")

    updated = service.update(
        reading.id,
        value=25,
        unit="C",
    )

    assert updated is not None
    assert updated.value == 25
    assert updated.unit == "C"


def test_delete_elimina_lectura() -> None:

    repo = FakeReadingRepository()
    service = ReadingService(repo)

    reading = service.record(1, 20, "C")

    deleted = service.delete(reading.id)

    assert deleted is True
    assert repo.get(reading.id) is None