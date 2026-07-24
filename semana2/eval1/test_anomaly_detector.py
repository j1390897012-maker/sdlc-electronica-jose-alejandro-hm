from anomaly_detector import AnomalyDetector
from sensor_reading import SensorReading


def test_detect_temperature_anomaly() -> None:
    detector = AnomalyDetector(
        max_temperature=35,
        max_humidity=80,
    )

    reading = SensorReading(
        sensor_id="TEMP-01",
        value=40,
        timestamp="2026-07-24 17:00",
    )

    assert detector.is_temperature_anomaly(reading)