# Sprint 1 Planning – Sistema Inteligente de Monitoreo Ambiental





## Sprint Goal

Implementar el núcleo funcional del sistema de monitoreo ambiental,
permitiendo registrar sensores, almacenar lecturas, detectar anomalías
y generar alertas para el operador.







## Historias seleccionadas

### US-02: Registrar un nuevo sensor
**Prioridad:** Must

**Justificación:**
Es necesario registrar sensores antes de poder almacenar
y consultar mediciones.

---

### US-04: Visualizar temperatura en tiempo real
**Prioridad:** Must

**Justificación:**
Representa la funcionalidad principal del sistema de monitoreo,
permitiendo visualizar las variables ambientales obtenidas por los sensores.
---

### US-01: Consultar historial de mediciones
**Prioridad:** Must

**Justificación:**
Permite analizar el comportamiento de los sensores a través del tiempo.

---

### US-07: Recibir alertas por valores críticos
**Prioridad:** Must

**Justificación:**
Permite detectar condiciones peligrosas y actuar oportunamente.

---

### US-08: Configurar umbrales de sensores
**Prioridad:** Must

**Justificación:**
Permite adaptar el sistema a diferentes condiciones de operación.

---

### US-10: Consultar estado de sensores
**Prioridad:** Should

**Justificación:**
Ayuda a verificar la disponibilidad y funcionamiento de los sensores.


## Tareas del Sprint

### US-02: Registrar un nuevo sensor

| Tarea | Tiempo estimado |
|---|---:|
| Diseñar la estructura del modelo Sensor | 2 h |
| Crear pruebas unitarias para el registro de sensores | 2 h |
| Implementar la lógica básica para registrar sensores | 3 h |
| Validar el registro de sensores duplicados | 2 h |


### US-04: Visualizar lecturas de sensores en tiempo real

| Tarea | Tiempo estimado |
|---|---:|
| Crear pruebas unitarias para la lectura de sensores | 2 h |
| Implementar la clase SensorReading | 3 h |
| Mostrar las lecturas actualizadas en tiempo real | 3 h |
| Validar la disponibilidad del sensor antes de leerlo | 2 h |

### US-01: Consultar historial de mediciones

| Tarea | Tiempo estimado |
|---|---:|
| Crear pruebas unitarias para consultar el historial | 2 h |
| Implementar la consulta del historial de mediciones | 3 h |
| Validar que el sensor exista antes de consultar | 1 h |
| Ordenar las mediciones por fecha y hora | 2 h |

### US-07: Recibir alertas por valores críticos

| Tarea | Tiempo estimado |
|---|---:|
| Crear pruebas unitarias para la detección de anomalías | 2 h |
| Implementar la clase AnomalyDetector | 3 h |
| Implementar la clase abstracta AlertManager | 2 h |
| Implementar ConsoleAlertManager y FileAlertManager | 3 h |
| Verificar la generación de alertas cuando se superan los umbrales | 2 h |

### US-08: Configurar umbrales de sensores

| Tarea | Tiempo estimado |
|---|---:|
| Crear pruebas unitarias para la configuración de umbrales | 2 h |
| Implementar el almacenamiento de umbrales por sensor | 3 h |
| Validar que los valores de umbral sean válidos | 2 h |
| Integrar los umbrales con AnomalyDetector | 2 h |

### US-10: Consultar estado de sensores

| Tarea | Tiempo estimado |
|---|---:|
| Crear pruebas unitarias para consultar el estado de un sensor | 2 h |
| Implementar la consulta del estado (Activo/Inactivo) | 2 h |
| Detectar sensores sin conexión | 3 h |
| Mostrar el estado del sensor al operador | 2 h |

## Definition of Done

Una historia de usuario se considera terminada cuando cumple con los siguientes criterios:

- Todos los criterios de aceptación (Gherkin) están implementados y verificados mediante pruebas.
- Todos los tests pasan correctamente.
- La cobertura de pruebas es igual o mayor al 80%.
- El código cumple las reglas de Ruff sin errores.
- El código pasa la verificación de MyPy sin errores.
- Los cambios fueron revisados mediante Pull Request antes de integrarse a la rama principal.
- La documentación correspondiente fue actualizada.