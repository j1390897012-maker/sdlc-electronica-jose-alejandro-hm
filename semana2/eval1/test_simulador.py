from simulador_sistema import SimuladorSistema, crear_sensores
from anomaly_detector import AnomalyDetector
from sensor_reading import SensorReading


def test_simulacion_10_sensores_60_ciclos():

    sensores = crear_sensores(10)

    sistema = SimuladorSistema(sensores)

    detector = AnomalyDetector(
        max_temperatura=35,
        max_humedad=80
    )

    lecturas_totales = 0
    alertas = 0

    for ciclo in range(60):

        lecturas = sistema.ejecutar_ciclo()

        for lectura in lecturas:
            lecturas_totales += 1

            if detector.is_temperature_anomaly(lectura):
                alertas += 1

    print(f"Lecturas totales: {lecturas_totales}")
    

    assert lecturas_totales == 600


class SensorSimuladorError:

    def __init__(self, sensor_id):
        self.sensor_id = sensor_id

    def obtener_lectura(self):

        return SensorReading(
            sensor_id=self.sensor_id,
            temperatura=40,
            humedad=60,
            timestamp="2026-07-25"
        )


def test_simulacion_detecta_alertas():

    sensores = [
        SensorSimuladorError("sensor_error")
    ]

    sistema = SimuladorSistema(sensores)

    detector = AnomalyDetector(
        max_temperatura=35,
        max_humedad=80
    )

    lecturas = sistema.ejecutar_ciclo()

    alertas = 0

    for lectura in lecturas:
        if detector.is_temperature_anomaly(lectura):
            alertas += 1
   
    print(f"Alertas detectadas: {alertas}")

    assert alertas == 1