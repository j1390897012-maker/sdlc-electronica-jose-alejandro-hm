"""Endpoints REST del recurso Alert."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.sql_alert_repository import SQLAlertRepository
from app.schemas.alert import AlertOut
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