"""Endpoints REST del recurso Alert."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.sql_alert_repository import SQLAlertRepository
from app.schemas.alert import AlertOut, AlertStatusUpdate
from app.services.alert_service import AlertService

router = APIRouter(
    tags=["alerts"],
)


def get_alert_service(
    db: Session = Depends(get_db),
) -> AlertService:
    """Inyecta un AlertService con el repositorio SQL real."""
    alert_repo = SQLAlertRepository(db)

    return AlertService(alert_repo)


@router.get(
    "/alerts",
    response_model=list[AlertOut],
)
def list_alerts(
    service: AlertService = Depends(get_alert_service),
) -> list[AlertOut]:
    """GET /alerts — lista todas las alertas registradas."""
    alerts = service.list()

    return [
        AlertOut.model_validate(alert)
        for alert in alerts
    ]

@router.patch(
    "/alerts/{alert_id}/status",
    response_model=AlertOut,
)
def update_alert_status(
    alert_id: int,
    data: AlertStatusUpdate,
    service: AlertService = Depends(get_alert_service),
) -> AlertOut:
    """PATCH /alerts/{alert_id} — actualiza el estado de una alerta."""


    try:
        
        alert = service.update_status(
        alert_id,
        data.status,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail=f"Alerta con id {alert_id} no encontrada.",
        )
    
    return AlertOut.model_validate(alert)