# ============================================
# ETAPA 1: BUILDER
# Instala dependencias de producción en un venv aislado
# y elimina lo que no hace falta en tiempo de ejecución
# (pip/setuptools/wheel solo sirven para instalar paquetes,
# no para correrlos; __pycache__ se regenera solo).
# ============================================
FROM python:3.12-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + \
    && rm -rf /opt/venv/lib/python3.12/site-packages/pip \
              /opt/venv/lib/python3.12/site-packages/pip-*.dist-info \
              /opt/venv/lib/python3.12/site-packages/setuptools \
              /opt/venv/lib/python3.12/site-packages/setuptools-*.dist-info \
              /opt/venv/lib/python3.12/site-packages/wheel \
              /opt/venv/lib/python3.12/site-packages/wheel-*.dist-info \
              /opt/venv/bin/pip*

# ============================================
# ETAPA 2: PRODUCCIÓN
# Imagen final: solo el venv ya instalado + el código
# estrictamente necesario para correr la API (sin tests/,
# scripts/, semana0-2/, .git, etc. -- ver .dockerignore).
# ============================================
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY app/ app/
COPY migrations/ migrations/
COPY alembic.ini .

EXPOSE 8000

# Comando de arranque con migraciones
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000