from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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
    response = client.post(
        "/readings/",
        json={
            "sensor_id": 1,
            "value": 25.5,
            "unit": "C",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["sensor_id"] == 1
    assert data["value"] == 25.5
    assert data["unit"] == "C"
    assert "id" in data

def test_post_reading_rechaza_cero_absoluto() -> None:
    response = client.post(
        "/readings/",
        json={
            "sensor_id": 1,
            "value": -300,
            "unit": "C",
        },
    )

    assert response.json()["detail"][0]["msg"] == (
    "Value error, El valor no puede estar por debajo del cero absoluto"
            )


def test_put_reading_actualiza_valor() -> None:
    response = client.post(
        "/readings/",
        json={
            "sensor_id": 2,
            "value": 20,
            "unit": "C",
        },
    )

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
    assert data["sensor_id"] == 2
    assert data["value"] == 25
    assert data["unit"] == "C"


def test_delete_reading_elimina_lectura() -> None:
    response = client.post(
        "/readings/",
        json={
            "sensor_id": 3,
            "value": 30,
            "unit": "C",
        },
    )

    reading_id = response.json()["id"]

    response = client.delete(
        f"/readings/{reading_id}",
    )

    assert response.status_code == 204

    response = client.get(
        f"/readings/{reading_id}",
    )

    assert response.status_code == 404