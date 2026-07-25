import random
from datetime import datetime

from sensor_reading import SensorReading


class GeneradorTemperatura:

    def __init__(self, media: float, desviacion: float)-> None:
        self.media = media
        self.desviacion = desviacion

    def generar(self)-> float:
        return random.normalvariate(
            self.media,
            self.desviacion
        )


class GeneradorHumedad:

    def __init__(self, media: float, desviacion: float)-> None:
        self.media = media
        self.desviacion = desviacion

    def generar(self)-> float:
        return random.normalvariate(
            self.media,
            self.desviacion
        )


class SensorSimulador:

    def __init__(
        self,
        media_temperatura: float,
        desviacion_temperatura: float,
        media_humedad: float,
        desviacion_humedad: float,
        sensor_id: str
    ) -> None:
        self.sensor_id = sensor_id

        self.generador_temperatura = GeneradorTemperatura(
            media_temperatura,
            desviacion_temperatura
        )

        self.generador_humedad = GeneradorHumedad(
            media_humedad,
            desviacion_humedad
        )

    def obtener_lectura(self)-> SensorReading:

        temperatura = self.generador_temperatura.generar()
        humedad = self.generador_humedad.generar()

        timestamp = datetime.now()

        return SensorReading(
            sensor_id=self.sensor_id,
            temperatura=temperatura,
            humedad=humedad,
            timestamp=str(timestamp)
        )