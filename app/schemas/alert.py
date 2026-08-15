""" Esquemas de alertas para la API. """

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    """ Representación de una alerta para la API. """
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: int
    reading_id: int
    value: float   
    threshold: float
    created_at: datetime
