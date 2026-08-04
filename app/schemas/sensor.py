"""Esquemas Pydantic (entrada/salida) del recurso Sensor."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.constants import VALID_UNITS

SensorType = Literal["temperature", "humidity", "pressure"]


class SensorCreate(BaseModel):
    """Datos requeridos para registrar un sensor nuevo (POST /sensors)."""

    name: str = Field(..., examples=["TEMP-01"])
    sensor_type: SensorType
    unit: str = Field(..., examples=["C"])

    @model_validator(mode="after")
    def validate_unit(self) -> "SensorCreate":
        """Rechaza unidades que no correspondan al tipo de sensor."""
        if self.unit not in VALID_UNITS[self.sensor_type]:
            raise ValueError(
                f"Unidad {self.unit!r} no válida para "
                f"{self.sensor_type!r}"
        )
        return self


class SensorUpdate(BaseModel):
    """Datos opcionales para actualización parcial (PATCH /sensors/{id})."""

    name: str | None = None
    sensor_type: SensorType | None = None
    unit: str | None = None

    @model_validator(mode="after")
    def validate_unit(self) -> "SensorUpdate":
        """Valida la combinación tipo/unidad solo si ambos vienen en el patch."""
        if self.sensor_type is None or self.unit is None:
            return self

        if self.unit not in VALID_UNITS[self.sensor_type]:
            raise ValueError(
                f"Unidad {self.unit!r} no válida para "
                f"{self.sensor_type!r}"
            )

        return self


class SensorOut(SensorCreate):
    """Representación de un sensor devuelta por la API, con su id."""

    id: int

    model_config = ConfigDict(from_attributes=True)