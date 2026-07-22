class SensorNotFoundError(Exception):
    pass


class SensorRegistry:

    def __init__(self):
        self.sensores = {}

    def get(self, sensor_id):
        self._validar_existencia(sensor_id)
        return self.sensores[sensor_id]

    def _validar_existencia(self, sensor_id):
        if sensor_id not in self.sensores:
            raise SensorNotFoundError(
                f"Sensor {sensor_id} no encontrado"
            )