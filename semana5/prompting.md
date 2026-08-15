
# Tarea 1: Conversión de Celsius a Fahrenheit

## Prompt Malo
**Petición:**  
Escribe una función que pase de Celsius a Fahrenheit.

**Respuesta:**
```python
def celsius_a_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32
```

---

## Prompt Bueno
**Contexto:**  
API FastAPI (Python 3.12) para gestión de sensores.

**Tarea:**  
Escribe una función pura `celsius_to_fahrenheit(c: float) -> float` en `semana5/conversions.py`.

**Restricciones:**
- Type hints completos
- Docstring
- Sin dependencias externas
- Redondeo a 2 decimales

**Entrega:**  
Solo la función, sin explicación.

**Respuesta:**
```python
def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit rounded to 2 decimal places."""
    return round((c * 9 / 5) + 32, 2)
```

---

# Tarea 2: Prueba para lectura inexistente

## Prompt Malo
**Petición:**  
Crea un test para una prueba para una lectura inexistente.

**Respuesta:**
```python
from fastapi.testclient import TestClient

def test_get_reading_no_existente(client: TestClient) -> None:
    response = client.get("/readings/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Lectura no encontrada"}
```

---

## Prompt Bueno
**Contexto:**  
API FastAPI en Python 3.12 para gestión de sensores, con arquitectura en capas y tests con pytest. El endpoint `GET /readings/{reading_id}` obtiene una lectura por su ID.

**Tarea:**  
Agrega un test en `tests/test_api.py` que compruebe que `GET /readings/999` devuelve HTTP 404 cuando la lectura no existe.

**Restricciones:**
- Utiliza el `TestClient` existente en el archivo
- No crees otro cliente
- No modifiques la aplicación
- Conserva el estilo de los tests existentes

**Entrega:**  
Solo el código del test.

**Respuesta:**
```python
def test_get_reading_no_existente() -> None:
    response = client.get("/readings/999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Lectura no encontrada"
    }
```

---

# Tarea 3: Crear una lectura asociada a un sensor

## Prompt Malo
**Petición:**  
Crea un test para crear una lectura de un sensor.

**Respuesta:**
```python
def test_post_reading() -> None:
    unique_name = f"TEMP-{uuid.uuid4().hex[:6]}"
    sensor_response = client.post(
        "/sensors/",
        json={
            "name": unique_name,
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 25.5,
            "unit": "C",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["sensor_id"] == sensor_id
    assert data["value"] == 25.5
    assert data["unit"] == "C"
    assert "id" in data
```

---

## Prompt Bueno
**Contexto:**  
API FastAPI en Python 3.12 para gestión de sensores. El proyecto utiliza SQLAlchemy 2.x tipado y arquitectura en capas con routers, schemas, services, repositories y models.

**Archivos relacionados con lecturas:**
- `app/routers/readings.py`
- `app/schemas/reading.py`
- `app/services/reading_service.py`
- `app/models/reading.py`

Los tests de API están en `tests/test_api.py`.

**Tarea:**  
Agrega un test que cree una lectura asociada a un sensor y compruebe que la respuesta contiene el `sensor_id` correcto, además de devolver HTTP 200 o el código de éxito que utilice actualmente el endpoint.

**Restricciones:**
- Utiliza las estructuras y fixtures existentes
- No inventes imports, clases, funciones ni endpoints
- No modifiques código de producción

**Entrega:**  
Solo el código del test.

**Respuesta:**
```python
def test_post_reading() -> None:
    unique_name = f"TEMP-{uuid.uuid4().hex[:6]}"
    sensor_response = client.post(
        "/sensors/",
        json={
            "name": unique_name,
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    sensor_id = sensor_response.json()["id"]

    response = client.post(
        f"/sensors/{sensor_id}/readings",
        json={
            "value": 25.5,
            "unit": "C",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["sensor_id"] == sensor_id
    assert data["value"] == 25.5
    assert data["unit"] == "C"
    assert "id" in data
```

---

# Conclusión

Los **prompts pobres** pueden producir código funcional, pero dejan muchas decisiones a criterio de la IA. Esto puede provocar que invente nombres de endpoints, imports, clases o estructuras que no existen en el proyecto.

Los **prompts buenos** proporcionan contexto, especifican exactamente la tarea, establecen restricciones y definen el formato de entrega. Esto reduce las suposiciones y hace que la respuesta sea más consistente con la arquitectura existente.
