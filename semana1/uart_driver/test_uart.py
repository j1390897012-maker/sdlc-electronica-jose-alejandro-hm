from config import UartConfig
import pytest

def test_uart_config():
    uart = UartConfig(
        baud_rate=9600,
        data_bits=8,
        stop_bits=1,
        parity='N'
    )
    assert uart.baud_rate == 9600
    assert uart.data_bits == 8
    assert uart.stop_bits == 1
    assert uart.parity == 'N'



def test_uart_config_invalid():
    with pytest.raises(ValueError):
        UartConfig(
            baud_rate=12345,  # Invalid baud rate
            data_bits=8,
            stop_bits=1,
            parity='N'
        )

