from pydantic import BaseModel


class MetricsOut(BaseModel):
    """Métricas básicas del estado actual de SensorHub."""

    sensors: int
    readings: int
    alerts: int
    alerts_open: int
    alerts_acknowledged: int
    alerts_resolved: int