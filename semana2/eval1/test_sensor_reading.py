from sensor_reading import SensorReading


def test_create_sensor_reading() -> None:
    reading = SensorReading(
    sensor_id="sensor_1",
    temperatura=25.5,
    humedad=60,
    timestamp="2026-07-25"
)

    assert reading.sensor_id == "sensor_1"
    assert reading.temperatura == 25.5
    assert reading.humedad == 60
    assert reading.timestamp == "2026-07-25"