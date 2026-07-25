from anomaly_detector import AnomalyDetector
from sensor_reading import SensorReading


def test_detect_temperatura_anomaly() -> None:
    detector = AnomalyDetector(
        max_temperatura=35,
        max_humedad=80,
    )
    reading = SensorReading(
    sensor_id="sensor_1",
    temperatura=36,
    humedad=60,
    timestamp="2026-07-25"
)
    assert detector.is_temperature_anomaly(reading)