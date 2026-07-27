from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/readings")
def readings():
    return [
        {
            "sensor_id": "TEMP-01",
            "temperature": 25.4,
            "humidity": 61.2,
        },
        {
            "sensor_id": "TEMP-02",
            "temperature": 27.1,
            "humidity": 58.9,
        },
    ]