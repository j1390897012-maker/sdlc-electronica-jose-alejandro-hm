"""Esquemas Pydantic (entrada/salida) del recurso Reading.

La validación de rango físico completa (que depende del tipo de
sensor, ej. humedad 0-100%) vive en ReadingService, porque Pydantic
por sí solo no conoce a qué sensor pertenece la lectura. Aquí solo
se valida la regla universal: nada por debajo del cero absoluto.
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SensorReadingIn(BaseModel):
    """Datos requeridos para registrar una lectura (POST /sensors/{id}/readings)."""

    value: float
    unit: str = Field(default="C", examples=["C"])

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: float) -> float:
        """Rechaza cualquier valor físicamente imposible (< -273.15)."""
        if value < -273.15:
            raise ValueError(
                "El valor no puede estar por debajo del cero absoluto"
            )

        return value


class SensorReadingUpdate(BaseModel):
    """Datos opcionales para actualización parcial (PATCH /readings/{id})."""

    value: float | None = None
    unit: str | None = None

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: float | None) -> float | None:
        """Misma validación de cero absoluto, solo si `value` viene en el patch."""
        if value is not None and value < -273.15:
            raise ValueError(
                "El valor no puede estar por debajo del cero absoluto"
            )

        return value


class SensorReadingOut(SensorReadingIn):
    """Representación de una lectura devuelta por la API, con su id."""

    sensor_id: int
    id: int

    model_config = ConfigDict(from_attributes=True)