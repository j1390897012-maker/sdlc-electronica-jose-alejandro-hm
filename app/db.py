"""Configuración del motor de base de datos y sesiones de SQLAlchemy.

En producción usa SQLite (sensorhub.db); los tests sobreescriben
`get_db` con una base de datos en memoria (ver tests/conftest.py).
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

engine = create_engine(
    "sqlite:///sensorhub.db"
)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Clase base declarativa de la que heredan todos los modelos ORM."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Dependencia de FastAPI que entrega una sesión de BD por request.

    Cierra la sesión automáticamente al terminar, incluso si la
    request lanza una excepción.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()