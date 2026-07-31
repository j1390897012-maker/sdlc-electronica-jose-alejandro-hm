from fastapi import APIRouter, Depends, HTTPException
from app.schemas.reading import SensorReadingIn, SensorReadingOut
from pydantic import BaseModel, ConfigDict, Field
from app.repositories.fake_reading_repository import FakeReadingRepository
from app.schemas.reading import SensorReadingIn
from app.services.reading_service import ReadingService

router = APIRouter(
    prefix="/readings",
    tags=["readings"],
)


repo = FakeReadingRepository()


def get_reading_service() -> ReadingService:
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