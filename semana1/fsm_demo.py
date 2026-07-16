class Estadobase:
    def __init__(self, duracion: int):
        self.duracion = duracion 
        self.tiempo_actual = 0

    def actualizar(self):
            self.tiempo_actual += 1 

    def termino(self) -> bool:
        return self.tiempo_actual >= self.duracion


class EstadoRojo(Estadobase):
    def __init__(self):
        super().__init__(30)
        


class EstadoVerde(Estadobase):
    def __init__(self):
        super().__init__(20)



class EstadoAmarillo(Estadobase):
    def __init__(self):
        super().__init__(5) 

class Semaforo:
    def __init__(self):
        self.rojo = EstadoRojo()
        self.verde = EstadoVerde()
        self.amarillo = EstadoAmarillo()
        self.estado_actual = self.rojo
    def avanzar(self):
        if self.estado_actual == self.rojo:
            self.estado_actual = self.verde
        elif self.estado_actual == self.verde:
            self.estado_actual = self.amarillo
        elif self.estado_actual == self.amarillo:
            self.estado_actual = self.rojo

         

