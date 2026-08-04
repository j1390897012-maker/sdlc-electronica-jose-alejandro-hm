"""Implementación en memoria de SensorRepository, solo para tests."""

from app.models.sensor import SensorModel


class FakeSensorRepository:
    """Doble de prueba de SensorRepository: guarda todo en una lista en memoria.

    Permite probar SensorService sin base de datos real (ver
    tests/test_sensor_service.py), pagando el DIP aplicado en el servicio.
    """

    def __init__(self) -> None:
        self.sensors: list[SensorModel] = []
        self.next_id = 1

    def add(
        self,
        name: str,
        sensor_type: str,
        unit: str,
    ) -> SensorModel:

        sensor = SensorModel(
            id=self.next_id,
            name=name,
            sensor_type=sensor_type,
            unit=unit,
        )

        self.sensors.append(sensor)
        self.next_id += 1

        return sensor

    def get(self, sensor_id: int) -> SensorModel | None:
        return next(
            (
                sensor
                for sensor in self.sensors
                if sensor.id == sensor_id
            ),
            None,
        )


    def get_by_name(self, name: str) -> SensorModel | None:
        return next(
        (
            sensor
            for sensor in self.sensors
            if sensor.name == name
        ),
            None,
    )



    def list(self) -> list[SensorModel]:
        return self.sensors

    def update(
        self,
        sensor_id: int,
        name: str | None = None,
        sensor_type: str | None = None,
        unit: str | None = None,
    ) -> SensorModel | None:

        sensor = self.get(sensor_id)

        if sensor is None:
            return None

        if name is not None:
            sensor.name = name

        if sensor_type is not None:
            sensor.sensor_type = sensor_type

        if unit is not None:
            sensor.unit = unit

        return sensor

    def delete(self, sensor_id: int) -> bool:
        sensor = self.get(sensor_id)

        if sensor is None:
            return False

        self.sensors.remove(sensor)
        return True