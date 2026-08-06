"""Endpoints REST del recurso Sensor (capa de presentación).

Solo traduce entre HTTP y SensorService: no contiene lógica de
negocio. Cada excepción de dominio (SensorDuplicadoError, ValueError,
sensor no encontrado) se mapea aquí a su código HTTP correspondiente.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.sql_sensor_repository import SQLSensorRepository
from app.schemas.sensor import SensorCreate, SensorOut, SensorUpdate
from app.services.sensor_service import SensorDuplicadoError, SensorService

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"],
)


def get_sensor_service(
    db: Session = Depends(get_db),
) -> SensorService:
    """Inyecta un SensorService con el repositorio SQL real (Depends)."""
    repo = SQLSensorRepository(db)
    return SensorService(repo)


@router.post(
    "/",
    response_model=SensorOut,
    status_code=201,
)
def create_sensor(
    sensor: SensorCreate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorOut:
    """POST /sensors — crea un sensor.

    409 si el nombre existe, 400 si la unidad no aplica al tipo.
    """
    try:
        result = service.create(
            sensor.name,
            sensor.sensor_type,
            sensor.unit,
            sensor.alert_threshold,
        )

        return SensorOut.model_validate(result)

    except SensorDuplicadoError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error
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
    """GET /sensors — lista todos los sensores registrados."""
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
    """GET /sensors/{id} — obtiene un sensor por id. 404 si no existe."""
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
    sensor: SensorUpdate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorOut:
    """PATCH /sensors/{id} — actualiza parcialmente un sensor.

    404 si no existe, 400 si la combinación tipo/unidad es inválida.
    """
    try:
        result = service.update(
            sensor_id,
            sensor.name,
            sensor.sensor_type,
            sensor.unit,
            sensor.alert_threshold,
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Sensor no encontrado",
            )

        return SensorOut.model_validate(result)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

@router.delete(
    "/{sensor_id}",
    status_code=204,
)
def delete_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
) -> None:
    """DELETE /sensors/{id} — elimina un sensor. 204 si se borró, 404 si no existía."""
    deleted = service.delete(sensor_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Sensor no encontrado",
        )