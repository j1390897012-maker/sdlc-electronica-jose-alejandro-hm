from semana0.hola_sensor import Sensor

def test_sensor_read_value() -> None:
    assert Sensor.read("TEMP-01") == 23.5