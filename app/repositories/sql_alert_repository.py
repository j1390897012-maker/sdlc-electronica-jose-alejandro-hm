
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import AlertModel


class SQLAlertRepository:
    """Implementación de AlertRepository respaldada por una base de datos SQL."""
    def __init__(self, session: Session) -> None:
        self._session = session
    
    def add(
        self,
        sensor_id: int,
        reading_id: int,
        value: float,
        threshold: float,
    ) -> AlertModel:
        
        alert = AlertModel(
            sensor_id=sensor_id,
            reading_id=reading_id,
            value=value,
            threshold=threshold,
        )
        self._session.add(alert)
        self._session.commit()
        self._session.refresh(alert)
        return alert
    
    
    def list(self) -> list[AlertModel]:
        statement = select(AlertModel)
        return list(self._session.scalars(statement).all())