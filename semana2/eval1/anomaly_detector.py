from sensor_reading import SensorReading


class AnomalyDetector:

    def __init__(
        self,
        max_temperatura: float,
        max_humedad: float,
    ) -> None:
        self.max_temperatura = max_temperatura
        self.max_humedad = max_humedad

    def is_temperature_anomaly(self, reading: SensorReading) -> bool:
        return reading.temperatura > self.max_temperatura

    def is_humidity_anomaly(self, reading: SensorReading) -> bool:
        return reading.humedad > self.max_humedad