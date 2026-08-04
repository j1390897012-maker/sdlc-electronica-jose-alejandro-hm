import pytest

from app.repositories.fake_sensor_repository import FakeSensorRepository
from app.services.sensor_service import SensorService


def create_service() -> SensorService:
    return SensorService(FakeSensorRepository())


def test_create_sensor() -> None:
    service = create_service()

    sensor = service.create(
        "TEMP-01",
        "temperature",
        "C",
    )

    assert sensor.id == 1
    assert sensor.name == "TEMP-01"
    assert sensor.sensor_type == "temperature"
    assert sensor.unit == "C"


def test_get_sensor() -> None:
    service = create_service()

    created = service.create(
        "TEMP-01",
        "temperature",
        "C",
    )

    sensor = service.get(created.id)

    assert sensor is not None
    assert sensor.name == "TEMP-01"


def test_list_sensors() -> None:
    service = create_service()

    service.create("TEMP-01", "temperature", "C")
    service.create("HUM-01", "humidity", "%")

    sensors = service.list()

    assert len(sensors) == 2


def test_update_sensor() -> None:
    service = create_service()

    created = service.create(
        "TEMP-01",
        "temperature",
        "C",
    )

    updated = service.update(
        created.id,
        name="TEMP-02",
        unit="F",
    )

    assert updated is not None
    assert updated.name == "TEMP-02"
    assert updated.unit == "F"


def test_delete_sensor() -> None:
    service = create_service()

    created = service.create(
        "TEMP-01",
        "temperature",
        "C",
    )

    assert service.delete(created.id) is True
    assert service.get(created.id) is None


def test_update_sensor_rechaza_unidad_incompatible() -> None:
    service = create_service()

    created = service.create(
        "TEMP-01",
        "temperature",
        "C",
    )

    with pytest.raises(ValueError):
        service.update(
            created.id,
            unit="%",
        )


def test_update_sensor_rechaza_cambio_de_tipo_incompatible() -> None:
    service = create_service()

    created = service.create(
        "TEMP-01",
        "temperature",
        "C",
    )

    with pytest.raises(ValueError):
        service.update(
            created.id,
            sensor_type="humidity",
        )


def test_create_sensor_con_umbral() -> None:
    service = create_service()

    sensor = service.create(
        "TEMP-01",
        "temperature",
        "C",
        alert_threshold=35.0,
    )

    assert sensor.alert_threshold == 35.0


def test_create_sensor_sin_umbral_queda_en_none() -> None:
    service = create_service()

    sensor = service.create(
        "TEMP-01",
        "temperature",
        "C",
    )

    assert sensor.alert_threshold is None


def test_update_sensor_cambia_el_umbral() -> None:
    service = create_service()

    created = service.create(
        "TEMP-01",
        "temperature",
        "C",
        alert_threshold=35.0,
    )

    updated = service.update(
        created.id,
        alert_threshold=40.0,
    )

    assert updated is not None
    assert updated.alert_threshold == 40.0