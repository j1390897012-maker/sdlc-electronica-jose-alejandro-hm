from collections.abc import Sequence
from typing import Protocol

from sensor_reading import SensorReading
from sensor_simulador import SensorSimulador


class Sensor(Protocol):
    def obtener_lectura(self) -> SensorReading:
        ...


class SimuladorSistema:
    def __init__(self, sensores: Sequence[Sensor]) -> None:
        self.sensores = sensores

    def ejecutar_ciclo(self)-> list[SensorReading]:
        lecturas = []
        for sensor in self.sensores:
            lectura = sensor.obtener_lectura()
            lecturas.append(lectura)
        return lecturas


def crear_sensores(cantidad: int)-> list[SensorSimulador]:
    sensores = []

    for i in range(cantidad):
        sensor = SensorSimulador(
            media_temperatura=25.5,
            desviacion_temperatura=3,
            media_humedad=60,
            desviacion_humedad=10,
            sensor_id=f"sensor_{i+1}"
        )

        sensores.append(sensor)
    return sensores



