from parser import *

def test_parse_uart_data():
    parser = ParserCSV()
    resltado = parser.parsear("datos de prueba")
    assert resltado == {"formato": "csv"}

def test_parse_JSON_data():
    parser = ParserJSON()
    resltado = parser.parsear("datos de prueba")
    assert resltado == {"formato": "json"}