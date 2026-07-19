import json


class Recorder:

    def guardar(self, datos):
        pass


class JsonLineRecorder(Recorder):

    def __init__(self, archivo):
        self.archivo = archivo


    def guardar(self, datos):

        with open(self.archivo, "a") as file:

            file.write(
                json.dumps(datos) + "\n"
            )

        return {
            "mensaje": "Datos guardados en JSON-lines"
        }