
from config import UartConfig
from device import UartDevice
from parsers import ModbusParser, NMEAParser

def test_uart_device_config():

    config = UartConfig(
        baud_rate=9600,
        data_bits=8,
        stop_bits=1,
        parity="N"
    )

    parser = ModbusParser()

    device = UartDevice(config, parser)

    assert device.config == config

def test_uart_device_modbus():

    config = UartConfig(
        baud_rate=9600,
        data_bits=8,
        stop_bits=1,
        parity="N"
    )

    parser = ModbusParser()

    device = UartDevice(config, parser)

    resultado = device.receive("TEMP:25")

    assert resultado["temperatura"] == 25

def test_uart_device_nmea():

    config = UartConfig(
        baud_rate=9600,
        data_bits=8,
        stop_bits=1,
        parity="N"
    )

    parser = NMEAParser()

    device = UartDevice(config, parser)

    resultado = device.receive(
        "GPS:19.432,-99.133"
    )

    assert resultado["latitud"] == 19.432