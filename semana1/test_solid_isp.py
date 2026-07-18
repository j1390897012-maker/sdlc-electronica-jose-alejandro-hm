from solid_isp_dip import ( SensorTemperatura, GuardarEnNube, EnviarPorWifi, MostrarEnPantalla)

def test_sensor_temperatura():
    sensor = SensorTemperatura()
    assert sensor.leer() == {"temperatura": 25}



def test_guardar_en_nube():
    almacenamiento = GuardarEnNube()
    datos = {"valor": 42}
    assert almacenamiento.guardar(datos) == {"mensaje": "Guardado en la nube"}