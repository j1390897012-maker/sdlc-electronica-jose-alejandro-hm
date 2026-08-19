"""Esquemas de alertas para la API."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class AlertStatus(str, Enum):
    """Estados permitidos para una alerta."""

    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class AlertOut(BaseModel):
    """Representación de una alerta para la API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: int
    reading_id: int
    value: float
    threshold: float
    created_at: datetime
    status: AlertStatus


class AlertStatusUpdate(BaseModel):
    """Datos para actualizar el estado de una alerta."""

    status: AlertStatus