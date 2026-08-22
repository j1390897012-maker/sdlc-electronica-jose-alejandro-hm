"""Notificación de alertas cuando una lectura supera su umbral (US-07).

Mismo patrón Strategy que ya usaste en semana2/eval1/alert_manager.py:
ReadingService depende de la abstracción AlertNotifier, no de una
implementación concreta, así que se puede sustituir en tests sin
tocar consola ni archivos (DIP).
"""

import logging
from typing import Protocol

logger = logging.getLogger(__name__)


class AlertNotifier(Protocol):
    """Contrato para cualquier forma de notificar una alerta."""

    def notify(self, message: str) -> None:
        """Envía una alerta con el mensaje dado."""
        ...


class ConsoleAlertNotifier:
    """Implementación por defecto: registra la alerta vía logging."""

    def notify(self, message: str) -> None:
        """Registra la alerta como log estructurado (nivel WARNING)."""
        logger.warning("alerta_generada", extra={"alert_message": message})


class FakeAlertNotifier:
    """Doble de prueba de AlertNotifier: guarda los mensajes en una lista
    en memoria en vez de imprimirlos, para poder verificarlos en los tests
    (ver tests/test_reading_service.py).
    """

    def __init__(self) -> None:
        self.messages: list[str] = []

    def notify(self, message: str) -> None:
        """Registra el mensaje de alerta en `self.messages`."""
        self.messages.append(message)
