# Ejemplo "mal" de SRP

class SistemaDeMonitoreo:
    def leer_sensor(self):
        pass

    def procesar_datos(self):
        pass

    def guardar_datos(self):
        pass

    def enviar_wifi(self):
        pass


# Ejemplo "bien" de SRP

class Sensor:
    def leer(self):
        return {"temperatura": 25, "humedad": 60}


class Procesador:
    def calcular(self, lectura):
        return {
            "temperatura_procesada": lectura["temperatura"] + 5,
            "humedad_procesada": lectura["humedad"] + 10,
        }


class Guardador:
    def guardar(self, datos):
        return {"mensaje": "Temp y Hum guardadas"}


class Wifi:
    def enviar(self, datos):
        return {"mensaje": "Temp y Hum enviadas"}


# Ejemplo "mal" de OCP

class ComunicacionMala:
    def enviar(self, datos, tipo):
        if tipo == "wifi":
            return {"mensaje": "Enviado por wifi"}
        elif tipo == "bluetooth":
            return {"mensaje": "Enviado por bluetooth"}
        elif tipo == "lora":
            return {"mensaje": "Enviado por LoRa"}


# Ejemplo "bien" de OCP

class Comunicacion:
    def enviar(self, datos):
        pass


class Wifi(Comunicacion):
    def enviar(self, datos):
        return {"mensaje": "Enviado por wifi"}


class Bluetooth(Comunicacion):
    def enviar(self, datos):
        return {"mensaje": "Enviado por bluetooth"}


class LoRa(Comunicacion):
    def enviar(self, datos):
        return {"mensaje": "Enviado por LoRa"}


# Ejemplo "mal" de LSP

class SensorBase:
    def leer(self):
        return {"valor": 0}


class SensorPresion(SensorBase):
    def leer(self):
        return {"presion": 1013}


class SensorPresionError(SensorBase):
    def leer(self):
        return {"error": "Sensor desconectado"}


# Ejemplo "bien" de LSP

class SensorLSP:
    def leer(self):
        pass


class SensorTemperatura(SensorLSP):
    def leer(self):
        return {"valor": 25}


class SensorHumedad(SensorLSP):
    def leer(self):
        return {"valor": 60}