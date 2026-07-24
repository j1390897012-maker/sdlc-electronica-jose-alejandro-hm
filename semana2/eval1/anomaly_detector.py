class AnomalyDetector:

    def __init__(
        self,
        max_temperature: float,
        max_humidity: float,
    ) -> None:
        self.max_temperature = max_temperature
        self.max_humidity = max_humidity

    def is_temperature_anomaly(self, reading) -> bool:
        return reading.value > self.max_temperature