from abc import ABC, abstractmethod


class MessageParser(ABC):

    @abstractmethod
    def parse(self, message):
        pass

class ModbusParser(MessageParser):

    def parse(self, message):

        try:
            temperatura = int(message.split(":")[1])

        except (IndexError, ValueError):
            raise ValueError("Mensaje Modbus inválido")

        return {
            "temperatura": temperatura,
            "protocolo": "Modbus"
        }


class NMEAParser(MessageParser):

    def parse(self, message):

        datos = message.split(":")[1]
        lat, lon = datos.split(",")

        return {
            "latitud": float(lat),
            "longitud": float(lon),
            "protocolo": "NMEA"
        }