from pydantic import BaseModel, ConfigDict, Field, field_validator


class SensorReadingIn(BaseModel):
    sensor_id: int = Field(..., examples=[1])
    value: float
    unit: str = Field(default="C", examples=["C"])

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: float) -> float:
        if value < -273.15:
            raise ValueError(
                "El valor no puede estar por debajo del cero absoluto"
            )

        return value


class SensorReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: float | None) -> float | None:
        if value is not None and value < -273.15:
            raise ValueError(
                "El valor no puede estar por debajo del cero absoluto"
            )

        return value


class SensorReadingOut(SensorReadingIn):
    id: int

    model_config = ConfigDict(from_attributes=True)