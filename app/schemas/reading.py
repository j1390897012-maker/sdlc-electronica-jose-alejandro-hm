from pydantic import BaseModel, ConfigDict, Field


class SensorReadingIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"


class SensorReadingOut(SensorReadingIn):
    id: int

    model_config = ConfigDict(from_attributes=True)