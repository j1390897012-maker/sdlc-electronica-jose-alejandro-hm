from solid_isp_dip import (
    SensorTemperatura,
    GuardarEnNube,
    NubeBien,
    MemoriaLocal,
    MonitoreoBien
)
def test_sensor_temperatura():
    sensor = SensorTemperatura()
    assert sensor.leer() == {"temperatura": 25}



def test_guardar_en_nube():
    almacenamiento = GuardarEnNube()
    datos = {"valor": 42}
    assert almacenamiento.guardar(datos) == {"mensaje": "Guardado en la nube"}

#test solid DIP

def test_monitoreo_guarda_en_nube():

    nube = NubeBien()

    sistema = MonitoreoBien(nube)

    resultado = sistema.guardar_datos({"temperatura":25})

    assert resultado == {"mensaje": "Guardado en la nube"}


def test_monitoreo_guarda_en_memoria_local():

    memoria = MemoriaLocal()

    sistema = MonitoreoBien(memoria)

    resultado = sistema.guardar_datos({"temperatura":25})

    assert resultado == {"mensaje": "Guardado en memoria local"}