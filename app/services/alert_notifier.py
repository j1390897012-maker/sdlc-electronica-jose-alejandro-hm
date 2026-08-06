"""Notificación de alertas cuando una lectura supera su umbral (US-07).

Mismo patrón Strategy que ya usaste en semana2/eval1/alert_manager.py:
ReadingService depende de la abstracción AlertNotifier, no de una
implementación concreta, así que se puede sustituir en tests sin
tocar consola ni archivos (DIP).
"""

from typing import Protocol


class AlertNotifier(Protocol):
    """Contrato para cualquier forma de notificar una alerta."""

    def notify(self, message: str) -> None:
        """Envía una alerta con el mensaje dado."""
        ...


class ConsoleAlertNotifier:
    """Implementación por defecto: imprime la alerta en consola."""

    def notify(self, message: str) -> None:
        """Imprime la alerta con el prefijo [ALERTA]."""
        print(f"[ALERTA] {message}")


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
