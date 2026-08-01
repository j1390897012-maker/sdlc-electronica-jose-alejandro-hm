from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.constants import VALID_UNITS

SensorType = Literal["temperature", "humidity", "pressure"]


class SensorCreate(BaseModel):
    name: str = Field(..., examples=["TEMP-01"])
    sensor_type: SensorType
    unit: str = Field(..., examples=["C"])

    @model_validator(mode="after")
    def validate_unit(self) -> "SensorCreate":
        if self.unit not in VALID_UNITS[self.sensor_type]:
            raise ValueError(
                f"Unidad {self.unit!r} no válida para "
                f"{self.sensor_type!r}"
        )
        return self


class SensorUpdate(BaseModel):
    name: str | None = None
    sensor_type: SensorType | None = None
    unit: str | None = None

    @model_validator(mode="after")
    def validate_unit(self) -> "SensorUpdate":
        if self.sensor_type is None or self.unit is None:
            return self

        if self.unit not in VALID_UNITS[self.sensor_type]:
            raise ValueError(
                f"Unidad {self.unit!r} no válida para "
                f"{self.sensor_type!r}"
            )

        return self


class SensorOut(SensorCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)