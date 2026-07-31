from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SensorCreate(BaseModel):
    name: str = Field(..., examples=["TEMP-01"])
    sensor_type: Literal["temperature", "humidity", "pressure"]
    unit: str = Field(..., examples=["C"])

    @model_validator(mode="after")
    def validate_unit(self) -> "SensorCreate":
        valid_units = {
            "temperature": {"C", "F"},
            "humidity": {"%"},
            "pressure": {"hPa"},
        }

        if self.unit not in valid_units[self.sensor_type]:
            raise ValueError(
                f"Unidad {self.unit!r} no vÃ¡lida para "
                f"{self.sensor_type!r}"
            )

        return self


class SensorOut(SensorCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)