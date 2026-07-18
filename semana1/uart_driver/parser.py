class Parser:
    def parsear(self, datos):
        pass

class ParserCSV(Parser):
    def parsear(self, datos):
        # Implementación específica para UART
        return {"formato": "csv"}

class ParserJSON(Parser):
    def parsear(self, datos):
        # Implementación específica para I2C
        return {"formato": "json"}

