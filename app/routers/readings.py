from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.sql_reading_repository import SQLReadingRepository
from app.schemas.reading import (
    SensorReadingIn,
    SensorReadingOut,
    SensorReadingUpdate,
)
from app.services.reading_service import ReadingService

router = APIRouter(
    prefix="/readings",
    tags=["readings"],
)


def get_reading_service(
    db: Session = Depends(get_db),
) -> ReadingService:
    repo = SQLReadingRepository(db)
    return ReadingService(repo)


@router.get("/{reading_id}", response_model=SensorReadingOut)
def get_reading(
    reading_id: int,
    service: ReadingService = Depends(get_reading_service),
) -> SensorReadingOut:
    reading = service.get_reading(reading_id)

    if reading is None:
        raise HTTPException(
            status_code=404,
            detail="Lectura no encontrada",
        )

    return SensorReadingOut.model_validate(reading)


@router.get(
    "/sensor/{sensor_id}",
    response_model=list[SensorReadingOut],
)
def list_readings_for_sensor(
    sensor_id: int,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    service: ReadingService = Depends(get_reading_service),
) -> list[SensorReadingOut]:

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


@router.post("/", response_model=SensorReadingOut, status_code=201)
def create_reading(
    reading: SensorReadingIn,
    service: ReadingService = Depends(get_reading_service),
) -> SensorReadingOut:
    try:
        result = service.record(
            reading.sensor_id,
            reading.value,
            reading.unit,
        )

        return SensorReadingOut.model_validate(result)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.patch("/{reading_id}", response_model=SensorReadingOut)
def update_reading(
    reading_id: int,
    reading: SensorReadingUpdate,
    service: ReadingService = Depends(get_reading_service),
) -> SensorReadingOut:
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

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.delete("/{reading_id}", status_code=204)
def delete_reading(
    reading_id: int,
    service: ReadingService = Depends(get_reading_service),
) -> None:
    deleted = service.delete(reading_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Lectura no encontrada",
        )