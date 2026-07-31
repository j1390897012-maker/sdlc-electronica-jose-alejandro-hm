from app.models.sensor import SensorModel
from app.repositories.sensor_repository import SensorRepository


class SensorService:

    def __init__(self, repo: SensorRepository) -> None:
        self._repo = repo

    def create(
        self,
        name: str,
        sensor_type: str,
        unit: str,
    ) -> SensorModel:

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

        return self._repo.update(
            sensor_id,
            name,
            sensor_type,
            unit,
        )

    def delete(self, sensor_id: int) -> bool:
        return self._repo.delete(sensor_id)