from app.repositories.fake_alert_repository import FakeAlertRepository
from app.services.alert_service import AlertService


def test_alerta_se_registra_y_puede_consultarse() -> None:
    repo = FakeAlertRepository()
    service = AlertService(repo)

    alert = service.create(
        sensor_id=1,
        reading_id=10,
        value=40.0,
        threshold=35.0,
    )

    assert alert.sensor_id == 1
    assert alert.reading_id == 10
    assert alert.value == 40.0
    assert alert.threshold == 35.0

    alerts = service.list()

    assert len(alerts) == 1
    assert alerts[0].id == alert.id

def test_alert_service_lista_vacio() -> None:
    repo = FakeAlertRepository()
    service = AlertService(repo)

    alerts = service.list()

    assert alerts == []