from sqlalchemy.orm import Session

from app.repositories.sql_alert_repository import SQLAlertRepository


def test_sql_alert_repository_registra_y_lista_alerta(
    session: Session,
) -> None:
    repo = SQLAlertRepository(session)

    alert = repo.add(
        sensor_id=1,
        reading_id=10,
        value=40.0,
        threshold=35.0,
    )

    assert alert.id is not None
    assert alert.sensor_id == 1
    assert alert.reading_id == 10
    assert alert.value == 40.0
    assert alert.threshold == 35.0

    alerts = repo.list()

    assert len(alerts) == 1
    assert alerts[0].id == alert.id


def test_sql_alert_repository_lista_vacio(
    session: Session,
) -> None:
    repo = SQLAlertRepository(session)

    alerts = repo.list()

    assert alerts == []