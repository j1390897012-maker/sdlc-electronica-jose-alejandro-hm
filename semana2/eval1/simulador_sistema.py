from sensor_simulador import SensorSimulador

class SimuladorSistema:
    def __init__(self, sensores):
        self.sensores = sensores

    def ejecutar_ciclo(self):
        lecturas = []
        for sensor in self.sensores:
            lectura = sensor.obtener_lectura()
            lecturas.append(lectura)
        return lecturas


def crear_sensores(cantidad):
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


