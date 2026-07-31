import uuid
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db() -> Generator[None, None, None]:
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )
    
    Base.metadata.create_all(bind=test_engine)
    
    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_reading_no_existente() -> None:
    response = client.get("/readings/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Lectura no encontrada"
    }




def test_post_sensor_duplicado_devuelve_409() -> None:
    sensor = {
        "name": "TEMP-DUPLICADO",
        "sensor_type": "temperature",
        "unit": "C",
    }
    primera_respuesta = client.post(
        "/sensors/",
        json=sensor,
    )

    assert primera_respuesta.status_code == 201

    segunda_respuesta = client.post(
        "/sensors/",
        json=sensor,
    )

    assert segunda_respuesta.status_code == 409
    assert segunda_respuesta.json() == {
        "detail": "Ya existe un sensor con nombre 'TEMP-DUPLICADO'"
    }


def test_crud_sensor_completo() -> None:
    sensor = {
        "name": "TEMP-CRUD",
        "sensor_type": "temperature",
        "unit": "C",
    }
    # Crear
    response = client.post(
        "/sensors/",
        json=sensor,
    )

    assert response.status_code == 201

    data = response.json()
    sensor_id = data["id"]

    assert data["name"] == "TEMP-CRUD"
    assert data["sensor_type"] == "temperature"
    assert data["unit"] == "C"

    # Listar
    response = client.get("/sensors/")

    assert response.status_code == 200

    sensors = response.json()

    assert any(
        item["id"] == sensor_id
        for item in sensors
    )

    # Obtener por ID
    response = client.get(
        f"/sensors/{sensor_id}",
    )

    assert response.status_code == 200
    assert response.json()["id"] == sensor_id

    # Actualizar
    response = client.patch(
        f"/sensors/{sensor_id}",
        json={
            "name": "TEMP-CRUD-ACTUALIZADO",
            "unit": "F",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == sensor_id
    assert data["name"] == "TEMP-CRUD-ACTUALIZADO"
    assert data["sensor_type"] == "temperature"
    assert data["unit"] == "F"

    # Eliminar
    response = client.delete(
        f"/sensors/{sensor_id}",
    )

    assert response.status_code == 204

    # Verificar que ya no existe
    response = client.get(
        f"/sensors/{sensor_id}",
    )

    assert response.status_code == 404


def test_list_readings_for_sensor_con_paginacion() -> None:
    sensor = {
        "name": "TEMP-PAGINACION",
        "sensor_type": "temperature",
        "unit": "C",
    }
    sensor_response = client.post(
        "/sensors/",
        json=sensor,
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    # Crear tres lecturas
    for value in (20, 21, 22):
        response = client.post(
            f"/sensors/{sensor_id}/readings",
            json={
                "value": value,
                "unit": "C",
            },
        )

        assert response.status_code == 201

    # Pedir las primeras dos
    response = client.get(
        f"/sensors/{sensor_id}/readings?limit=2&offset=0",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert [reading["value"] for reading in data] == [20, 21]

    # Saltar las dos primeras y pedir las siguientes
    response = client.get(
        f"/sensors/{sensor_id}/readings?limit=2&offset=2",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["value"] == 22





def test_post_reading() -> None:
    unique_name = f"TEMP-{uuid.uuid4().hex[:6]}"
    sensor_response = client.post(
        "/sensors/",
        json={
            "name": unique_name,
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 25.5,
            "unit": "C",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["sensor_id"] == sensor_id
    assert data["value"] == 25.5
    assert data["unit"] == "C"
    assert "id" in data





def test_post_reading_rechaza_unidad_invalida() -> None:
    unique_name = f"TEMP-{uuid.uuid4().hex[:6]}"

    sensor_response = client.post(
        "/sensors/",
        json={
            "name": unique_name,
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 25,
            "unit": "%",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "Unidad '%' no válida para "
            "sensor de tipo 'temperature'"
        )
    }





def test_post_reading_rechaza_humedad_fuera_de_rango() -> None:
    unique_name = f"HUM-{uuid.uuid4().hex[:6]}"

    sensor_response = client.post(
        "/sensors/",
        json={
            "name": unique_name,
            "sensor_type": "humidity",
            "unit": "%",
        },
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 101,
            "unit": "%",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "La humedad debe estar entre 0 y 100"
    }



def test_post_reading_sensor_no_existe() -> None:
    response = client.post(
        "/sensors/999/readings",
        json={
            "value": 25,
            "unit": "C",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Sensor no encontrado"
    }




def test_post_reading_rechaza_cero_absoluto() -> None:
    unique_name = f"TEMP-{uuid.uuid4().hex[:6]}"
    sensor_response = client.post(
        "/sensors/",
        json={
            "name": unique_name,
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": -300,
            "unit": "C",
        },
    )

    assert response.status_code == 422

    detail = response.json()["detail"]

    assert detail[0]["msg"] == (
        "Value error, El valor no puede estar por debajo del "
        "cero absoluto"
    )


def test_put_reading_actualiza_valor() -> None:
    unique_name = f"TEMP-{uuid.uuid4().hex[:6]}"
    sensor_response = client.post(
        "/sensors/",
        json={
            "name": unique_name,
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 20,
            "unit": "C",
        },
    )

    assert response.status_code == 201

    reading_id = response.json()["id"]

    response = client.patch(
        f"/readings/{reading_id}",
        json={
            "value": 25,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == reading_id
    assert data["sensor_id"] == sensor_id
    assert data["value"] == 25
    assert data["unit"] == "C"


def test_delete_reading_elimina_lectura() -> None:
    unique_name = f"TEMP-{uuid.uuid4().hex[:6]}"
    sensor_response = client.post(
        "/sensors/",
        json={
            "name": unique_name,
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 30,
            "unit": "C",
        },
    )

    assert response.status_code == 201

    reading_id = response.json()["id"]

    response = client.delete(
        f"/readings/{reading_id}",
    )

    assert response.status_code == 204

    response = client.get(
        f"/readings/{reading_id}",
    )

    assert response.status_code == 404