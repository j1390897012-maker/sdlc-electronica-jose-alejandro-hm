from device import UartDevice
from config import UartConfig
from parser import ParserCSV, ParserJSON

def test_uart_device_CSV():
    config = UartConfig(
        baud_rate=9600,
        data_bits=8,
        stop_bits=1,
        parity='N'
    )

    parser = ParserCSV()

    uart = UartDevice(config, parser)

    resultado = uart.recibir_datos("25.7")

    assert resultado["formato"] == "csv"


def test_uart_device_JSON():
        config = UartConfig(
            baud_rate=9600,
            data_bits=8,
            stop_bits=1,
            parity='N'
        )

        parser = ParserJSON()

        uart = UartDevice(config, parser)

        resultado = uart.recibir_datos("24.54")
        assert resultado["formato"] == "json"
