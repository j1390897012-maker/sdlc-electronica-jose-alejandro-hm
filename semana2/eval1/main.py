from alert_manager import AlertManager, ConsoleAlert
from anomaly_detector import AnomalyDetector
from simulador_sistema import SimuladorSistema, crear_sensores


def main() -> None:
    sensores = crear_sensores(10)
    sistema = SimuladorSistema(sensores)

    detector = AnomalyDetector(
        max_temperatura=35,
        max_humedad=80,
    )

    alert_manager = AlertManager(ConsoleAlert())

    for ciclo in range(60):
        lecturas = sistema.ejecutar_ciclo()

        for lectura in lecturas:
            if detector.is_temperature_anomaly(lectura):
                alert_manager.alert(
                    f"[Ciclo {ciclo}] Temperatura crítica en "
                    f"{lectura.sensor_id}: {lectura.temperatura:.1f}°C"
                )

            if detector.is_humidity_anomaly(lectura):
                alert_manager.alert(
                    f"[Ciclo {ciclo}] Humedad crítica en "
                    f"{lectura.sensor_id}: {lectura.humedad:.1f}%"
                )


if __name__ == "__main__":
    main()