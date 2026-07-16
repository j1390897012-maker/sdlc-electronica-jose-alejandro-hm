from fsm_demo import Semaforo

def test_semaforo_inicia_en_rojo():
    semaforo = Semaforo()  
    assert semaforo.estado_actual == semaforo.rojo


def test_avanzar_cambia_estado():
    semaforo = Semaforo()
    semaforo.avanzar()
    assert semaforo.estado_actual == semaforo.verde

def test_avanzar_ciclo_completo():
    semaforo = Semaforo()
    semaforo.avanzar()  # Rojo -> Verde 
    semaforo.avanzar()  # Verde -> Amarillo
    assert semaforo.estado_actual == semaforo.amarillo
def test_avanzar_ciclo_completo_retorna_a_rojo():
    semaforo = Semaforo()
    semaforo.avanzar()  # Rojo -> Verde 
    semaforo.avanzar()  # Verde -> Amarillo
    semaforo.avanzar()  # Amarillo -> Rojo
    assert semaforo.estado_actual == semaforo.rojo