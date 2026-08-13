import pytest

from app.repositories.fake_reading_repository import (
    FakeReadingRepository,
)
from app.repositories.fake_sensor_repository import (
    FakeSensorRepository,
)
from app.services.alert_notifier import FakeAlertNotifier
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


def test_record_dispara_alerta_si_supera_umbral() -> None:
    reading_repo = FakeReadingRepository()
    sensor_repo = FakeSensorRepository()
    notifier = FakeAlertNotifier()

    sensor_repo.add(
        "TEMP-01",
        "temperature",
        "C",
        alert_threshold=35.0,
    )

    service = ReadingService(
        reading_repo,
        sensor_repo,
        notifier,
    )

    reading = service.record(
        sensor_id=1,
        value=40.0,
        unit="C",
    )

    assert reading.alert_triggered is True
    assert len(notifier.messages) == 1
    assert "TEMP-01" in notifier.messages[0]
    assert "40" in notifier.messages[0]


def test_record_no_dispara_alerta_si_no_supera_umbral() -> None:
    reading_repo = FakeReadingRepository()
    sensor_repo = FakeSensorRepository()
    notifier = FakeAlertNotifier()

    sensor_repo.add(
        "TEMP-01",
        "temperature",
        "C",
        alert_threshold=35.0,
    )

    service = ReadingService(
        reading_repo,
        sensor_repo,
        notifier,
    )

    reading = service.record(
        sensor_id=1,
        value=20.0,
        unit="C",
    )

    assert reading.alert_triggered is False
    assert notifier.messages == []


def test_record_sin_umbral_configurado_nunca_alerta() -> None:
    """Un sensor sin alert_threshold (None) nunca dispara alertas,
    sin importar qué tan alto sea el valor registrado."""
    reading_repo = FakeReadingRepository()
    sensor_repo = FakeSensorRepository()
    notifier = FakeAlertNotifier()

    sensor_repo.add(
        "TEMP-01",
        "temperature",
        "C",
    )

    service = ReadingService(
        reading_repo,
        sensor_repo,
        notifier,
    )

    reading = service.record(
        sensor_id=1,
        value=999.0,
        unit="C",
    )

    assert reading.alert_triggered is False
    assert notifier.messages == []


def test_record_sensor_inexistente() -> None:
    with pytest.raises(LookupError, match="Sensor no encontrado"):
        create_service().record(sensor_id=999, value=25.5, unit="C")


def test_record_temperatura_cero_absoluto() -> None:
    service = create_service()
    reading = service.record(sensor_id=1, value=-273.15, unit="C")
    assert reading.value == -273.15


def test_record_exactamente_en_el_alert_threshold() -> None:
    sensor_repo = FakeSensorRepository()
    sensor_repo.add("TEMP-01", "temperature", "C", alert_threshold=35.0)
    service = ReadingService(FakeReadingRepository(), sensor_repo)
    reading = service.record(sensor_id=1, value=35.0, unit="C")
    assert not reading.alert_triggered


def test_record_slightly_above_alert_threshold() -> None:
    sensor_repo = FakeSensorRepository()
    sensor_repo.add(
        "TEMP-01",
        "temperature",
        "C",
        alert_threshold=35.0,
    )
    service = ReadingService(
        FakeReadingRepository(),
        sensor_repo,
        FakeAlertNotifier(),
    )

    reading = service.record(
        sensor_id=1,
        value=35.0001,
        unit="C",
    )

    assert reading.alert_triggered is True


def test_record_unidad_invalida() -> None:
    with pytest.raises(ValueError):
        create_service().record(
            sensor_id=1,
            value=25.5,
            unit="K",
        )
