"""Configuración centralizada de logging estructurado (RNF-5).

Expone logs en formato JSON (un objeto por línea) para que puedan ser
parseados por herramientas externas (Render, Docker logs, etc.). El
nivel de log se controla exclusivamente por la variable de entorno
``LOG_LEVEL`` (por defecto ``INFO``), sin valores hardcodeados en el
código de negocio.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import UTC, datetime
from typing import Any


class JsonFormatter(logging.Formatter):
    """Formatea cada registro de log como una línea JSON."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        # Permite adjuntar campos extra vía logger.info(..., extra={...})
        reserved = logging.LogRecord(
            "", 0, "", 0, "", (), None
        ).__dict__.keys()
        for key, value in record.__dict__.items():
            if key not in reserved and key not in payload:
                payload[key] = value

        return json.dumps(payload, default=str)


def configure_logging() -> None:
    """Configura el logging raíz de la aplicación.

    El único parámetro configurable es el nivel, tomado de la
    variable de entorno ``LOG_LEVEL`` (INFO por defecto). No requiere
    ni acepta ninguna otra fuente de configuración.
    """
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)
