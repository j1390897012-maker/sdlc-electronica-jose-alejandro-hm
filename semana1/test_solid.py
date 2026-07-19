from solid_srp_ocp_lsp import (
    Sensor,
    Procesador,
    Wifi,
    Bluetooth,
    LoRa,
    SensorTemperatura,
    SensorHumedad,
)


# Tests para SRP

def test_sensor_lectura():
    sensor = Sensor()

    assert sensor.leer() == {
        "temperatura": 25,
        "humedad": 60
    }


def test_procesador_calculo():
    procesador = Procesador()

    lectura = {
        "temperatura": 25,
        "humedad": 60
    }

    resultado = procesador.calcular(lectura)

    assert resultado == {
        "temperatura_procesada": 30,
        "humedad_procesada": 70
    }


# Tests para OCP

def test_wifi_envio():
    wifi = Wifi()

    resultado = wifi.enviar("temp")

    assert resultado["mensaje"] == "Enviado por wifi"


def test_bluetooth_envio():
    bluetooth = Bluetooth()

    resultado = bluetooth.enviar("temp")

    assert resultado["mensaje"] == "Enviado por bluetooth"


def test_lora_envio():
    lora = LoRa()

    resultado = lora.enviar("temp")

    assert resultado["mensaje"] == "Enviado por LoRa"


# Tests para LSP

def test_sensor_temperatura():
    sensor = SensorTemperatura()

    resultado = sensor.leer()

    assert resultado["valor"] == 25


def test_sensor_humedad():
    sensor = SensorHumedad()

    resultado = sensor.leer()

    assert resultado["valor"] == 60