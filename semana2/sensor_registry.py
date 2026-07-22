class SensorNotFoundError(Exception):
    pass

class SensorRegistry:

    def __init__(self):
        self.sensors = {}
    def get(self, sensor_id):


        if sensor_id not in self.sensors:
            raise SensorNotFoundError()

        return self.sensores[sensor_i]
