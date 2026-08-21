from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_empty_database(client: TestClient) -> None:
    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert data["sensors"] == 0
    assert data["readings"] == 0
    assert data["alerts"] == 0
    assert data["alerts_open"] == 0
    assert data["alerts_acknowledged"] == 0
    assert data["alerts_resolved"] == 0

def test_metrics_reflect_system_state(client: TestClient) -> None:
    sensor_response = client.post(
        "/sensors/",
        json={
            "name": "TEMP-METRICS",
            "sensor_type": "temperature",
            "unit": "C",
            "alert_threshold": 30,
        },
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    for value in (20, 25, 40):
        response = client.post(
            f"/sensors/{sensor_id}/readings",
            json={
                "value": value,
                "unit": "C",
            },
        )

        assert response.status_code == 201

    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert data["sensors"] == 1
    assert data["readings"] == 3
    assert data["alerts"] == 1
    assert data["alerts_open"] == 1
    assert data["alerts_acknowledged"] == 0
    assert data["alerts_resolved"] == 0


def test_metrics_alert_status_changes(client: TestClient) -> None:
    sensor_response = client.post(
        "/sensors/",
        json={
            "name": "TEMP-METRICS-STATUS",
            "sensor_type": "temperature",
            "unit": "C",
            "alert_threshold": 30,
        },
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    reading_response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 40,
            "unit": "C",
        },
    )

    assert reading_response.status_code == 201

    metrics = client.get("/metrics")
    assert metrics.status_code == 200

    data = metrics.json()

    assert data["alerts"] == 1
    assert data["alerts_open"] == 1
    assert data["alerts_acknowledged"] == 0
    assert data["alerts_resolved"] == 0

    alerts_response = client.get("/alerts")

    assert alerts_response.status_code == 200

    alert_id = alerts_response.json()[0]["id"]

    update_response = client.patch(
        f"/alerts/{alert_id}/status",
        json={"status": "acknowledged"},
    )

    assert update_response.status_code == 200

    metrics = client.get("/metrics")
    data = metrics.json()

    assert data["alerts"] == 1
    assert data["alerts_open"] == 0
    assert data["alerts_acknowledged"] == 1
    assert data["alerts_resolved"] == 0

    update_response = client.patch(
        f"/alerts/{alert_id}/status",
        json={"status": "resolved"},
    )

    assert update_response.status_code == 200

    metrics = client.get("/metrics")
    data = metrics.json()

    assert data["alerts"] == 1
    assert data["alerts_open"] == 0
    assert data["alerts_acknowledged"] == 0
    assert data["alerts_resolved"] == 1