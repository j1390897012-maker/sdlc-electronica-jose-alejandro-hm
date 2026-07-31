from fastapi import FastAPI

from app.db import Base, engine
from app.models.reading import ReadingModel
from app.routers import readings

app = FastAPI(title="SensorHub API", version="0.1.0")

app.include_router(readings.router)

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}