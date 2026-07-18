from dataclasses import dataclass

BAUDRATES_VALIDOS = [9600, 19200, 38400, 57600, 115200]

BITS_VALIDOS = [5, 6, 7, 8]

STOP_BITS_VALIDOS = [1, 2]

PARITY_VALIDOS = ['N', 'E', 'O']  # N: None, E: Even, O: Odd


@dataclass(frozen=True)
class UartConfig:
    baud_rate: int
    data_bits: int
    stop_bits: int
    parity: str

    def __post_init__(self):
        if self.baud_rate not in BAUDRATES_VALIDOS:
            raise ValueError(f"Baud rate inválido: {self.baud_rate}. Debe ser uno de {BAUDRATES_VALIDOS}.")
        if self.data_bits not in BITS_VALIDOS:
            raise ValueError(f"Data bits inválido: {self.data_bits}. Debe ser uno de {BITS_VALIDOS}.")
        if self.stop_bits not in STOP_BITS_VALIDOS:
            raise ValueError(f"Stop bits inválido: {self.stop_bits}. Debe ser uno de {STOP_BITS_VALIDOS}.")
        if self.parity not in PARITY_VALIDOS:
            raise ValueError(f"Paridad inválida: {self.parity}. Debe ser uno de {PARITY_VALIDOS}.")

