# ============================================
# ETAPA 1: BUILDER
# ============================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Copiar y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# ETAPA 2: PRODUCCIÓN
# ============================================
FROM python:3.12-slim

WORKDIR /app

# Copiar solo lo necesario desde builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar el código de la aplicación
COPY . .

EXPOSE 8000

# Comando de arranque con migraciones
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000