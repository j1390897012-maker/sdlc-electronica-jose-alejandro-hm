from solid_isp_dip import ( SensorTemperatura, GuardarEnNube, EnviarPorWifi, MostrarEnPantalla, Nube, MemoriaLocal, Monitoreo)

def test_sensor_temperatura():
    sensor = SensorTemperatura()
    assert sensor.leer() == {"temperatura": 25}



def test_guardar_en_nube():
    almacenamiento = GuardarEnNube()
    datos = {"valor": 42}
    assert almacenamiento.guardar(datos) == {"mensaje": "Guardado en la nube"}

#test solid DIP


def test_monitoreo_guarda_en_nube():

    nube = Nube()

    sistema = Monitoreo(nube)

    resultado = sistema.guardar_datos("temperatura")

    assert resultado["mensaje"] == "Guardado en la nube"


def test_monitoreo_guarda_en_memoria_local():

    memoria = MemoriaLocal()

    sistema = Monitoreo(memoria)

    resultado = sistema.guardar_datos("temperatura")

    assert resultado["mensaje"] == "Guardado en memoria local"