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

class SensorTemperatura(DispositivoIoT):
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
        