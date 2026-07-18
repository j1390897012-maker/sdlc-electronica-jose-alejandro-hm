from config import UartConfig
from parser import Parser

class UartDevice:
    def __init__(self, config, parser):
        self.config = config
        self.parser = parser 
    
    def recibir_datos(self, datos):
        return self.parser.parsear(datos)

       