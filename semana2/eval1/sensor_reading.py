from dataclasses import dataclass


@dataclass
class SensorReading:
    sensor_id: str
    value: float
    timestamp: str