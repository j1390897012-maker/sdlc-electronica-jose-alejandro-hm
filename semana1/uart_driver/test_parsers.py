from parsers import ModbusParser, NMEAParser
import pytest
################### Test_ModbusParser
def test_modbus_parser():

    parser = ModbusParser()

    resultado = parser.parse("TEMP:25")

    assert resultado["temperatura"] == 25
    assert resultado["protocolo"] == "Modbus"

def test_modbus_parser_diferente_valor():

    parser = ModbusParser()

    resultado = parser.parse("TEMP:30")

    assert resultado["temperatura"] == 30

def test_modbus_parser_error():

    parser = ModbusParser()

    with pytest.raises(ValueError):
        parser.parse("ERROR")

##############Test_ModbusParser

def test_nmea_parser():

    parser = NMEAParser()

    resultado = parser.parse(
        "GPS:19.432,-99.133"
    )

    assert resultado["latitud"] == 19.432
    assert resultado["longitud"] == -99.133
    assert resultado["protocolo"] == "NMEA"

def test_nmea_parser_otras_coordenadas():

    parser = NMEAParser()

    resultado = parser.parse(
        "GPS:20.0,-100.0"
    )

    assert resultado["latitud"] == 20.0

def test_nmea_parser_error():

    parser = NMEAParser()

    with pytest.raises(ValueError):
        parser.parse("GPS:error")

