# sdlc-electronica-jose-alejandro-hm
## Reflexión SOLID

# SensorHub API

API REST para telemetría IoT con detección de anomalías y gestión de sensores.

## 🚀 Estado del Proyecto

| Métrica | Estado |
|---|---|
| **CI/CD** | [![CI](https://github.com/j1390897012-maker/sdlc-electronica-jose-alejandro-hm/actions/workflows/ci.yml/badge.svg)](https://github.com/j1390897012-maker/sdlc-electronica-jose-alejandro-hm/actions/workflows/ci.yml) |
| **Despliegue** | [![Render](https://img.shields.io/badge/Render-Live-brightgreen)](https://sensorhub-api-mgri.onrender.com) |
| **Cobertura** | ≥ 80% |

## 🌐 API en Producción

- **URL base:** https://sensorhub-api-mgri.onrender.com
- **Healthcheck:** https://sensorhub-api-mgri.onrender.com/health
- **Documentación (Swagger):** https://sensorhub-api-mgri.onrender.com/docs

## 📦 Requisitos

- Python 3.12+
- Docker y Docker Compose
- Git

## 🛠️ Instalación y Ejecución Local

### Opción 1: Con Docker Compose (recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/j1390897012-maker/sdlc-electronica-jose-alejandro-hm.git
cd sdlc-electronica-jose-alejandro-hm

# Levantar API + PostgreSQL
docker-compose up --build