"""Configuración del motor de base de datos y sesiones de SQLAlchemy.

En producción usa SQLite (sensorhub.db); los tests sobreescriben
`get_db` con una base de datos en memoria (ver tests/conftest.py).
"""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


def get_database_url() -> str:  
    url = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db") 
    ## busca la variable de entorno DATABASE_URL, 
    # si no existe usa SQLite por defecto

    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1) 
        ## Cambia el esquema de la URL de conexión a 
        # PostgreSQL para usar psycopg como driver
    
    if url.startswith("postgresql://") and "+psycopg" not in url: 
        ## Si el URL comienza con "postgresql://" y no contiene "+psycopg", 
        # reemplaza el esquema para usar psycopg como driver
        return url.replace("postgresql://", "postgresql+psycopg://", 1)

    return url
       







engine = create_engine(
    get_database_url()
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