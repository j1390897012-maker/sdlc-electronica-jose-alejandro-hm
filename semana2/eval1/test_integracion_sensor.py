from sensor_reading import SensorReading
from anomaly_detector import AnomalyDetector


def test_detecta_temperatura_alta() -> None:
    detector = AnomalyDetector(
        max_temperatura=35,
        max_humedad=80
    )

    reading = SensorReading(
    sensor_id="sensor_1",
    temperatura=36,
    humedad=60,
    timestamp="2026-07-25"
)

    resultado = detector.is_temperature_anomaly(reading)

    assert resultado is True


def test_no_detecta_temperatura_normal() -> None:
    detector = AnomalyDetector(
        max_temperatura=35,
        max_humedad=80
    )

    reading = SensorReading(
    sensor_id="sensor_1",
    temperatura=26,
    humedad=60,
    timestamp="2026-07-25"
)

    assert detector.is_temperature_anomaly(reading) is False