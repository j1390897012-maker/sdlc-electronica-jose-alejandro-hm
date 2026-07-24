from sensor_reading import SensorReading





def test_create_sensor_reading() -> None:
    reading = SensorReading(
        sensor_id="TEMP-01",
        value=25.5,
        timestamp="2026-07-24 16:30"
    )

    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 25.5
    assert reading.timestamp == "2026-07-24 16:30"