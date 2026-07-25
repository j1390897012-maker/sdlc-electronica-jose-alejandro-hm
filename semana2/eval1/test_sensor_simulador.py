from sensor_reading import SensorReading
from sensor_simulador import SensorSimulador


def test_sensor_simulador()-> None:
    simulador = SensorSimulador(
    media_temperatura=25.5,
    desviacion_temperatura=3,
    media_humedad=60,
    desviacion_humedad=10,
    sensor_id="sensor_1"
)
    reading = simulador.obtener_lectura()
    assert isinstance(reading, SensorReading)
    assert 18 <= reading.temperatura <= 33
    assert 40 <= reading.humedad <= 80
    
