

class SensorReading:
    def __init__(
        self, 
        sensor_id: str,
         value: float,
          timestamp:str) -> None:
        self.sensor_id = sensor_id
        self.value = value
        self.timestamp = timestamp
        


