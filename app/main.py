from fastapi import FastAPI

from app.db import Base, engine
from app.routers import readings, sensors

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SensorHub API",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(sensors.router)
app.include_router(readings.router)