"""Punto de entrada de la API SensorHub.

Crea la instancia de FastAPI, registra los routers de cada recurso
y asegura que las tablas existan en la base de datos al arrancar.
Se ejecuta con: uvicorn app.main:app --reload
"""

import logging

from fastapi import FastAPI

from app.db import Base, engine
from app.logging_config import configure_logging
from app.routers import alerts, metrics, readings, sensors

configure_logging()
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SensorHub API",
    version="0.1.0",
)


@app.on_event("startup")
def log_startup() -> None:
    """Registra el arranque de la aplicación (RNF-5: logs estructurados)."""
    logger.info("sensorhub_api_startup")


@app.get("/health")
def health() -> dict[str, str]:
    """Endpoint de salud para verificar que la API está corriendo."""
    return {"status": "ok"}


app.include_router(sensors.router)
app.include_router(readings.router)
app.include_router(alerts.router)
app.include_router(metrics.router)