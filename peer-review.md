# Peer Review — Semana 3

## Qué revisar

1. Arquitectura en 4 capas
2. Separación Router → Service → Repository → Model
3. Validaciones Pydantic
4. Códigos HTTP 400/404/409/422
5. CRUD de sensores y lecturas
6. Paginación
7. Inyección de dependencias
8. Tests de integración con TestClient
9. Cobertura mínima del 80 %
10. Ruff y MyPy

## Cómo probar

pytest -q
ruff check .
mypy app