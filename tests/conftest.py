"""Fixtures globales de pytest para las pruebas de integración de la API.

Estas fixtures crean una base de datos SQLite en memoria, aislada por test,
y sobreescriben la dependencia `get_db` de FastAPI para que cada prueba
corra contra una base de datos limpia sin tocar la base real (sensorhub.db).
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
def setup_test_db() -> Generator[None, None, None]:
    """Crea las tablas antes de cada test y las destruye al terminar.

    `autouse=True` para que todos los tests de este paquete la usen
    automáticamente sin tener que declararla como parámetro.
    """
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


@pytest.fixture
def client() -> TestClient:
    """Cliente de pruebas de FastAPI, ya conectado a la base de datos de test."""
    return TestClient(app)
