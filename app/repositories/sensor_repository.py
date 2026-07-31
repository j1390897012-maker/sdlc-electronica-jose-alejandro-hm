from typing import Protocol

from app.models.sensor import SensorModel


class SensorRepository(Protocol):

    def add(
        self,
        name: str,
        sensor_type: str,
        unit: str,
    ) -> SensorModel:
        ...

    def get(self, sensor_id: int) -> SensorModel | None:
        ...

    def list(self) -> list[SensorModel]:
        ...

    def update(
        self,
        sensor_id: int,
        name: str | None = None,
        sensor_type: str | None = None,
        unit: str | None = None,
    ) -> SensorModel | None:
        ...

    def delete(self, sensor_id: int) -> bool:
        ...