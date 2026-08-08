"""Smoke test de producción: crea sensor, crea lectura y verifica alerta.

Se ejecuta en CI contra PostgreSQL como service (ver .github/workflows/ci.yml),
después de `alembic upgrade head`. Usa la capa de servicios real
(SensorService / ReadingService) en vez de tocar los modelos ORM
directamente, para ejercitar la misma lógica de negocio que corre en
producción -- incluyendo el cálculo de `alert_triggered`.

Sale con código distinto de cero (vía excepción no capturada) si algo
falla, para que el job de GitHub Actions se marque en rojo.
"""

from app.db import SessionLocal
from app.repositories.sql_reading_repository import SQLReadingRepository
from app.repositories.sql_sensor_repository import SQLSensorRepository
from app.services.reading_service import ReadingService
from app.services.sensor_service import SensorService

SENSOR_NAME = "SMOKE-TEST-01"
ALERT_THRESHOLD = 30.0
READING_VALUE = 35.5  # > ALERT_THRESHOLD a propósito, para forzar la alerta


def main() -> None:
    db = SessionLocal()

    try:
        sensor_repo = SQLSensorRepository(db)
        reading_repo = SQLReadingRepository(db)

        sensor_service = SensorService(sensor_repo)
        reading_service = ReadingService(reading_repo, sensor_repo)

        # 1. Crear sensor
        sensor = sensor_service.create(
            name=SENSOR_NAME,
            sensor_type="temperature",
            unit="C",
            alert_threshold=ALERT_THRESHOLD,
        )
        assert sensor.id is not None, "El sensor no recibió un id autogenerado"
        print(f"✅ Sensor creado: id={sensor.id}, name={sensor.name!r}")

        # 2. Crear lectura (usando el id REAL del sensor, no su nombre)
        reading = reading_service.record(
            sensor_id=sensor.id,
            value=READING_VALUE,
            unit="C",
        )
        print(
            f"✅ Lectura creada: id={reading.id}, value={reading.value}, "
            f"created_at={reading.created_at}"
        )

        # 3. Consultar alerta
        if not reading.alert_triggered:
            raise AssertionError(
                f"Se esperaba alert_triggered=True "
                f"({READING_VALUE} > {ALERT_THRESHOLD}), "
                f"pero quedó en {reading.alert_triggered}"
            )
        print(
            f"✅ Alerta verificada: alert_triggered={reading.alert_triggered} "
            f"({READING_VALUE} > {ALERT_THRESHOLD})"
        )

        # 4. Confirmar que la lectura quedó asociada al sensor correcto
        readings = reading_service.list_for_sensor(sensor.id)
        assert len(readings) == 1, (
            f"Se esperaba 1 lectura para el sensor, se encontraron {len(readings)}"
        )
        print(f"✅ Consulta por sensor confirmada: {len(readings)} lectura(s)")

    finally:
        db.close()


if __name__ == "__main__":
    main()