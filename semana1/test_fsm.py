from fsm_demo import EstadoRojo

def test_estado_rojo_duracion():
    rojo = EstadoRojo()
    assert rojo.duracion == 30


def test_estado_inicia_en_cero():
    rojo = EstadoRojo()
    assert rojo.tiempo_actual == 0

def test_estado_actualiza_tiempo():
    rojo = EstadoRojo()
    rojo.actualizar()
    assert rojo.tiempo_actual == 1

def test_estado_termino():
    rojo = EstadoRojo()
    for _ in range(30):
        rojo.actualizar()
    assert rojo.termino() is True