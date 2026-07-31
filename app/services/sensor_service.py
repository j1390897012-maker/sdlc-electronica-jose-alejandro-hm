from app.models.sensor import SensorModel
from app.repositories.sensor_repository import SensorRepository


class SensorDuplicadoError(Exception):
    pass


class SensorService:

    def __init__(self, repo: SensorRepository) -> None:
        self._repo = repo

    def create(
        self,
        name: str,
        sensor_type: str,
        unit: str,
    ) -> SensorModel:

        if self._repo.get_by_name(name) is not None:
            raise SensorDuplicadoError(
                f"Ya existe un sensor con nombre {name!r}"
            )

        return self._repo.add(
            name,
            sensor_type,
            unit,
        )

    def get(self, sensor_id: int) -> SensorModel | None:
        return self._repo.get(sensor_id)

    def list(self) -> list[SensorModel]:
        return self._repo.list()

    def update(
        self,
        sensor_id: int,
        name: str | None = None,
        sensor_type: str | None = None,
        unit: str | None = None,
    ) -> SensorModel | None:

        sensor = self._repo.get(sensor_id)

        if sensor is None:
            return None

        new_sensor_type = (
            sensor_type
            if sensor_type is not None
            else sensor.sensor_type
        )

        new_unit = (
            unit
            if unit is not None
            else sensor.unit
        )

        valid_units = {
            "temperature": {"C", "F"},
            "humidity": {"%"},
            "pressure": {"hPa"},
        }

        if new_unit not in valid_units[new_sensor_type]:
            raise ValueError(
                f"Unidad {new_unit!r} no válida para "
                f"{new_sensor_type!r}"
            )

        return self._repo.update(
            sensor_id,
            name,
            sensor_type,
            unit,
        )

    def delete(self, sensor_id: int) -> bool:
        return self._repo.delete(sensor_id)