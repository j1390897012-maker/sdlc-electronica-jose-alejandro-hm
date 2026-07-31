from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException

from app.db import SessionLocal
from app.repositories.sql_sensor_repository import SQLSensorRepository
from app.schemas.sensor import SensorCreate, SensorOut
from app.services.sensor_service import SensorService

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"],
)


def get_sensor_service() -> Generator[SensorService, None, None]:
    session = SessionLocal()

    try:
        repo = SQLSensorRepository(session)
        yield SensorService(repo)
    finally:
        session.close()

@router.post(
    "/",
    response_model=SensorOut,
    status_code=201,
)
def create_sensor(
    sensor: SensorCreate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorOut:
    try:
        result = service.create(
            sensor.name,
            sensor.sensor_type,
            sensor.unit,
        )

        return SensorOut.model_validate(result)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@router.get(
    "/",
    response_model=list[SensorOut],
)
def list_sensors(
    service: SensorService = Depends(get_sensor_service),
) -> list[SensorOut]:
    sensors = service.list()

    return [
        SensorOut.model_validate(sensor)
        for sensor in sensors
    ]


@router.get(
    "/{sensor_id}",
    response_model=SensorOut,
)
def get_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
) -> SensorOut:
    sensor = service.get(sensor_id)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor no encontrado",
        )

    return SensorOut.model_validate(sensor)


@router.patch(
    "/{sensor_id}",
    response_model=SensorOut,
)
def update_sensor(
    sensor_id: int,
    sensor: SensorCreate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorOut:
    result = service.update(
        sensor_id,
        sensor.name,
        sensor.sensor_type,
        sensor.unit,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor no encontrado",
        )

    return SensorOut.model_validate(result)


@router.delete(
    "/{sensor_id}",
    status_code=204,
)
def delete_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
) -> None:
    deleted = service.delete(sensor_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Sensor no encontrado",
        )