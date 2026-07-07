from semana0.hola_sensor import Sensor

def test_sensor_read_returns_23_5() -> None:
    sensor = Sensor()
    assert sensor.read() == 23.5