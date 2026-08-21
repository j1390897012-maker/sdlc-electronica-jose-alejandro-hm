"""Endpoints operacionales de salud y métricas de SensorHub."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.alert import AlertModel
from app.models.reading import ReadingModel
from app.models.sensor import SensorModel
from app.schemas.metrics import MetricsOut

router = APIRouter(
    tags=["metrics"],
)


@router.get(
    "/metrics",
    response_model=MetricsOut,
)
def get_metrics(
    db: Session = Depends(get_db),
) -> MetricsOut:
    """Devuelve métricas básicas del estado de SensorHub."""

    sensors = db.scalar(
        select(func.count()).select_from(SensorModel)
    ) or 0

    readings = db.scalar(
        select(func.count()).select_from(ReadingModel)
    ) or 0

    alerts = db.scalar(
        select(func.count()).select_from(AlertModel)
    ) or 0

    alerts_open = db.scalar(
        select(func.count()).select_from(AlertModel).where(
            AlertModel.status == "open"
        )
    ) or 0

    alerts_acknowledged = db.scalar(
        select(func.count()).select_from(AlertModel).where(
            AlertModel.status == "acknowledged"
        )
    ) or 0

    alerts_resolved = db.scalar(
        select(func.count()).select_from(AlertModel).where(
            AlertModel.status == "resolved"
        )
    ) or 0

    return MetricsOut(
        sensors=sensors,
        readings=readings,
        alerts=alerts,
        alerts_open=alerts_open,
        alerts_acknowledged=alerts_acknowledged,
        alerts_resolved=alerts_resolved,
    )