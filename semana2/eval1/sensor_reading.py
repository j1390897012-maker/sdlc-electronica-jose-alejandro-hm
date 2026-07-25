from dataclasses import dataclass


@dataclass
class SensorReading:
    sensor_id: str
    temperatura: float
    humedad: float
    timestamp: str