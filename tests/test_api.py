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