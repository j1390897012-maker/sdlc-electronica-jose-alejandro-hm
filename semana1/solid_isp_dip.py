# #Ejemplo "mal" de ISP

class DispositivoIoT:
    def leer(self):
        return {"valor": 0}
    def enviar(self, datos):
        return {"mensaje": "Enviado por wifi"}
    def guardar(sekf, datos):
        return {"mensaje": "Guardado en la nube"}

    def mostrar(self):
        return {"mensaje": "Mostrando datos en pantalla"}

class SensorTemperaturamal(DispositivoIoT):
    def leer(self):
        return {"temperatura": 25}


##Ejemplo "bien" de ISP

class Lectura:
    def leer(self):
        return {"valor": 0}

class Almacenamiento:
    def guardar(self, datos):
        return {"mensaje": "Guardado en la nube"}

class Comunicacion:
    def enviar(self, datos):
        return {"mensaje": "Enviado por wifi"}

class Pantalla:
    def mostrar(self):
        return {"mensaje": "Mostrando datos en pantalla"}

class SensorTemperatura(Lectura):
    def leer(self):
        return {"temperatura": 25}

class GuardarEnNube(Almacenamiento):
    def guardar(self, datos):
        return {"mensaje": "Guardado en la nube"}

class EnviarPorWifi(Comunicacion):
    def enviar(self, datos):
        return {"mensaje": "Enviado por wifi"}

class MostrarEnPantalla(Pantalla):
    def mostrar(self):
        return {"mensaje": "Mostrando datos en pantalla"}


# Ejemplo "mal" de DIP

class Nube:
    def guardar(self, datos):
        return {"mensaje": "Guardado en la nube"}


class MemoriaLocalMal:
    def guardar(self, datos):
        return {"mensaje": "Guardado en memoria local"}


class Monitoreo:
    def __init__(self):
        self.nube = Nube()
        self.memoria = MemoriaLocal()

    def guardar_datos(self, datos, tipo):
        if tipo == "nube":
            return self.nube.guardar(datos)

        elif tipo == "local":
            return self.memoria.guardar(datos)

#Ejemplo "bien" de DIP

class Almacenamiento:
    def guardar(self, datos):
        pass

class NubeBien(Almacenamiento):
    def guardar(self, datos):
        return {"mensaje": "Guardado en la nube"}

class MemoriaLocal(Almacenamiento):
    def guardar(self, datos):
        return {"mensaje": "Guardado en memoria local"}

class MonitoreoBien:
    def __init__(self, almacenamiento):
        self.almacenamiento = almacenamiento

    def guardar_datos(self, datos):
        return self.almacenamiento.guardar(datos)