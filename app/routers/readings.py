"""Endpoints REST del recurso Reading (capa de presentación).

Solo traduce entre HTTP y ReadingService: no contiene lógica de
negocio. LookupError (sensor no existe) se mapea a 404 y ValueError
(unidad o rango físico inválido) se mapea a 400.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.sql_alert_repository import SQLAlertRepository
from app.repositories.sql_reading_repository import SQLReadingRepository
from app.repositories.sql_sensor_repository import SQLSensorRepository
from app.schemas.reading import (
    SensorReadingIn,
    SensorReadingOut,
    SensorReadingUpdate,
)
from app.services.alert_service import AlertService
from app.services.reading_service import ReadingService

router = APIRouter(
    tags=["readings"],
)


def get_reading_service(
    db: Session = Depends(get_db),
) -> ReadingService:
    """Inyecta un ReadingService con los repositorios SQL reales (Depends)."""
    reading_repo = SQLReadingRepository(db)
    sensor_repo = SQLSensorRepository(db)
    alert_repo = SQLAlertRepository(db)
    alert_service = AlertService(alert_repo)

    return ReadingService(
        reading_repo,
        sensor_repo,
        alert_service=alert_service
    )



@router.get(
    "/sensors/{sensor_id}/readings/stats",
)
def get_reading_stats(
    sensor_id: int,
    date_from: datetime | None = Query(default=None, alias="from"),
    date_to: datetime | None = Query(default=None, alias="to"),
    service: ReadingService = Depends(get_reading_service),
) -> dict[str, float]:
    """GET /sensors/{id}/readings/stats — estadísticas por periodo."""

    try:
        return service.get_stats_for_sensor(
            sensor_id,
            date_from,
            date_to,
        )

    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error



@router.get(
    "/readings/{reading_id}",
    response_model=SensorReadingOut,
)
def get_reading(
    reading_id: int,
    service: ReadingService = Depends(get_reading_service),
) -> SensorReadingOut:
    """GET /readings/{id} — obtiene una lectura por id. 404 si no existe."""
    reading = service.get_reading(reading_id)

    if reading is None:
        raise HTTPException(
            status_code=404,
            detail="Lectura no encontrada",
        )

    return SensorReadingOut.model_validate(reading)


@router.get(
    "/sensors/{sensor_id}/readings",
    response_model=list[SensorReadingOut],
)
def list_readings_for_sensor(
    sensor_id: int,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    date_from: datetime | None = Query(default=None, alias="from"),
    date_to: datetime | None = Query(default=None, alias="to"),
    service: ReadingService = Depends(get_reading_service),
) -> list[SensorReadingOut]:
    """GET /sensors/{id}/readings — paginado, con filtro `from`/`to`."""
    readings = service.list_for_sensor(
        sensor_id,
        limit,
        offset,
        date_from,
        date_to,
    )

    return [
        SensorReadingOut.model_validate(reading)
        for reading in readings
    ]


@router.post(
    "/sensors/{sensor_id}/readings",
    response_model=SensorReadingOut,
    status_code=201,
)
def create_reading(
    sensor_id: int,
    reading: SensorReadingIn,
    service: ReadingService = Depends(get_reading_service),
) -> SensorReadingOut:
    """POST /sensors/{id}/readings — registra una lectura.

    404 si el sensor no existe, 400 si el valor/unidad es inválido.
    """
    try:
        result = service.record(
            sensor_id,
            reading.value,
            reading.unit,
        )

        return SensorReadingOut.model_validate(result)

    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.patch(
    "/readings/{reading_id}",
    response_model=SensorReadingOut,
)
def update_reading(
    reading_id: int,
    reading: SensorReadingUpdate,
    service: ReadingService = Depends(get_reading_service),
) -> SensorReadingOut:
    """PATCH /readings/{id} — actualiza parcialmente una lectura.

    404 si no existe, 400 si el resultado es inválido.
    """
    try:
        result = service.update(
            reading_id,
            reading.value,
            reading.unit,
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Lectura no encontrada",
            )

        return SensorReadingOut.model_validate(result)

    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.delete(
    "/readings/{reading_id}",
    status_code=204,
)
def delete_reading(
    reading_id: int,
    service: ReadingService = Depends(get_reading_service),
) -> None:
    """DELETE /readings/{id} — elimina una lectura (204, o 404 si no existía)."""
    deleted = service.delete(reading_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Lectura no encontrada",
        )