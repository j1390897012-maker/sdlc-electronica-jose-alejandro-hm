

# AI Code Review — ReadingService

## Contexto

Se realizó un code review asistido por IA sobre la clase
`app/services/reading_service.py`.

El objetivo fue identificar posibles:

- Violaciones de SOLID.
- Casos borde sin manejar.
- Riesgos de seguridad.
- Problemas de rendimiento.
- Oportunidades de mejora.

La IA utilizada para la revisión fue Qwen 2.5 Coder 7B mediante Aider.

La revisión no se aceptó automáticamente. Cada hallazgo fue investigado
y evaluado antes de decidir si debía implementarse.

---

# Hallazgos

## Hallazgo 1 — Uso de `LookupError` para sensor inexistente

### Propuesta de la IA

La IA señaló que `_validate_reading()` utiliza:

```python
raise LookupError("Sensor no encontrado")
````

y propuso crear una excepción específica como `SensorNotFoundError`.

También señaló que utilizar directamente `HTTPException` dentro del service
sería una mala opción porque acoplaría la lógica de negocio con FastAPI.

### Investigación

Se revisó cómo se comunican actualmente las capas de la aplicación y cómo
los routers manejan las excepciones provenientes de los servicios.

También se consideró la diferencia entre una excepción propia de dominio y
una excepción HTTP.

Crear una excepción específica sería una mejora posible, pero también
implicaría modificar el service, el router y potencialmente los tests que
dependen del comportamiento actual.

### Decisión

**Rechazado por ahora.**

### Justificación

El comportamiento actual es funcional y está cubierto mediante pruebas.
Cambiar la excepción no corrige un defecto actual y aumentaría el alcance
del cambio.

Además, se considera correcto mantener la capa de servicio independiente
de FastAPI y evitar introducir `HTTPException` directamente en ella.

La creación de excepciones específicas puede quedar como mejora futura si
el proyecto necesita distinguir diferentes errores de dominio de forma más
precisa.

---

## Hallazgo 2 — Validación de unidades y rangos físicos en `ReadingService`

### Propuesta de la IA

La IA señaló que `_validate_reading()` contiene reglas específicas para
temperatura, humedad y presión:

```python
if sensor.sensor_type == "temperature":
    ...

elif sensor.sensor_type == "humidity":
    ...

elif sensor.sensor_type == "pressure":
    ...
```

Propuso mover esta lógica al modelo `SensorModel` o crear un componente
externo como `ReadingValidator`.

La razón indicada fue una posible violación de SRP y OCP, ya que agregar
nuevos tipos de sensores requeriría modificar `ReadingService`.

### Investigación

Se revisó la responsabilidad actual de `ReadingService` y el motivo por
el cual la validación se encuentra allí.

La validación no depende únicamente del valor recibido: necesita consultar
primero el sensor para conocer su tipo y posteriormente aplicar las reglas
correspondientes.

También se consideró que mover la lógica al modelo podría aumentar la
responsabilidad del modelo y acoplar reglas de negocio adicionales a esa
capa.

### Decisión

**Rechazado por ahora.**

### Justificación

La implementación actual mantiene la validación encapsulada dentro del
servicio y evita modificar varias capas del sistema.

Aunque la propuesta de separar las reglas puede ser válida desde el punto
de vista de extensibilidad, actualmente no existe un problema que justifique
el refactor.

Además, modificar esta parte tendría un alcance mayor y requeriría ampliar
la batería de pruebas.

Se considera una posible mejora arquitectónica futura si aumenta el número
de tipos de sensores o las reglas de validación se vuelven más complejas.

---

## Hallazgo 3 — Validación del `alert_threshold`

### Propuesta de la IA

La IA señaló que `_check_alert()` compara directamente:

```python
if value <= sensor.alert_threshold:
    return False
```

y observó que podría existir un sensor configurado con un umbral que no
tenga sentido para su tipo.

Por ejemplo, un sensor de humedad podría configurarse con un umbral mayor
que 100.

### Investigación

Se revisó la responsabilidad de `_check_alert()`.

El método actualmente tiene como responsabilidad evaluar si una lectura
supera un umbral ya configurado, no validar la configuración del sensor.

También se revisó que la validación del umbral pertenece conceptualmente al
momento en que se crea o modifica la configuración del sensor.

### Decisión

**Aceptado como mejora futura, pero no implementado en este ejercicio.**

### Justificación

El hallazgo es válido, pero modificar `_check_alert()` no sería la solución
más adecuada.

La validación debería realizarse cuando se configura o modifica
`alert_threshold`, evitando que una configuración inválida llegue al
servicio de lecturas.

Por lo tanto, se considera una mejora válida para `SensorService`, pero
queda fuera del alcance de este ejercicio para evitar introducir cambios
innecesarios.

---

## Hallazgo 4 — `update()` no recalcula `alert_triggered`

### Propuesta de la IA

La IA señaló que al actualizar una lectura no se recalcula
`alert_triggered`.

Propuso recalcular la alerta después de modificar el valor.

### Investigación

Se revisó el comportamiento documentado directamente en `ReadingService`.

El método `update()` contiene explícitamente la decisión de diseño:

```text
Las alertas se evalúan al momento de ingesta (`record`);
editar una lectura ya guardada no reabre ni reemite una alerta
retroactivamente.
```

Por lo tanto, el comportamiento observado por la IA no es accidental.

### Decisión

**Rechazado.**

### Justificación

La IA identificó una diferencia de comportamiento, pero la interpretó como
un posible defecto cuando en realidad se trata de una decisión de diseño
documentada.

Recalcular la alerta durante una actualización cambiaría el comportamiento
actual de la aplicación y podría provocar notificaciones retroactivas no
deseadas.

Por esta razón, no se modificó el código.

---

## Hallazgo 5 — Comportamiento de `delete()` cuando la lectura no existe

### Propuesta de la IA

La IA señaló que:

```python
def delete(self, reading_id: int) -> bool:
    return self._repo.delete(reading_id)
```

devuelve simplemente `False` cuando la lectura no existe.

Propuso lanzar una excepción específica o devolver la lectura eliminada.

### Investigación

Se revisó el contrato actual del repositorio y del servicio.

El método ya utiliza `bool` como resultado para indicar si la eliminación
fue realizada correctamente.

Cambiar este contrato requeriría modificar las capas que consumen el
servicio y sus correspondientes tests.

### Decisión

**Rechazado por ahora.**

### Justificación

El comportamiento actual es sencillo, explícito y suficiente para el
alcance actual de la aplicación.

No existe evidencia de un problema funcional que obligue a cambiar el
contrato.

La propuesta podría ser considerada en una futura revisión de diseño de
errores de la API, pero no se considera necesaria en este momento.

---

## Hallazgo 6 — `VALID_UNITS` como estructura mutable

### Propuesta de la IA

La IA señaló que:

```python
from app.constants import VALID_UNITS
```

utiliza una estructura global mutable y propuso utilizar `Enum`,
`frozenset` u otra estructura inmutable.

### Investigación

Se revisó el uso actual de `VALID_UNITS`.

La estructura se utiliza como una constante de configuración y no se
modifica durante la ejecución normal de la aplicación.

Aunque una estructura inmutable podría expresar mejor la intención de
"constante", no existe actualmente un flujo que modifique el diccionario.

### Decisión

**Rechazado por ahora.**

### Justificación

Se considera una mejora de diseño, pero no un defecto funcional actual.

Cambiar la estructura requeriría revisar todos los lugares donde se utiliza
y podría generar cambios innecesarios para el objetivo del ejercicio.

---

## Hallazgo 7 — Nombre de `_validate_reading()`

### Propuesta de la IA

La IA observó que `_validate_reading()` además de validar devuelve el sensor
obtenido:

```python
return sensor
```

y propuso renombrarlo a algo como:

```python
_validate_and_get_sensor()
```

### Investigación

Se revisó el flujo de `record()`:

```python
sensor = self._validate_reading(...)
alert_triggered = self._check_alert(sensor, value)
```

El sensor se devuelve intencionalmente para evitar realizar otra consulta al
repositorio.

### Decisión

**Rechazado por ahora.**

### Justificación

El nombre podría ser más descriptivo, pero la implementación evita una
segunda consulta innecesaria al repositorio.

No existe un problema funcional y el cambio únicamente sería de
nomenclatura.

Se considera una mejora de legibilidad que puede realizarse junto con un
refactor futuro.

---

## Hallazgo 8 — `ConsoleAlertNotifier` como valor predeterminado

### Propuesta de la IA

La IA señaló:

```python
self._notifier = notifier or ConsoleAlertNotifier()
```

y propuso eliminar el valor predeterminado o utilizar un `NullNotifier`.

### Investigación

Se revisó el sistema de inyección de dependencias y los tests existentes.

El constructor permite inyectar `FakeAlertNotifier` durante las pruebas,
mientras que `ConsoleAlertNotifier` proporciona un comportamiento
predeterminado cuando no se proporciona un notifier.

Esto evita que el servicio falle cuando se utiliza sin un notifier explícito.

### Decisión

**Rechazado por ahora.**

### Justificación

La propuesta podría ser apropiada para una aplicación con un sistema de
notificaciones de producción más desarrollado, pero actualmente el
`ConsoleAlertNotifier` cumple una función útil como implementación
predeterminada.

No se encontró un defecto que justifique eliminarlo.

---

## Hallazgo 9 — Concurrencia al registrar lecturas

### Propuesta de la IA

La IA señaló que `record()` no contiene mecanismos explícitos de control
de concurrencia y sugirió revisar las transacciones del repositorio.

### Investigación

Se revisó la separación entre `ReadingService` y los repositorios.

El servicio no administra directamente las transacciones de base de datos;
esa responsabilidad pertenece a la capa de persistencia.

Por lo tanto, introducir mecanismos de concurrencia directamente en
`ReadingService` podría romper la separación de responsabilidades.

### Decisión

**Rechazado para este ejercicio.**

### Justificación

El hallazgo es válido como punto de revisión arquitectónica, pero no se
identificó un defecto demostrable en `ReadingService`.

La concurrencia debe analizarse posteriormente en el repositorio y en la
configuración de SQLAlchemy/transacciones.

No se realizaron cambios porque hacerlo desde este servicio no sería la
solución adecuada.

---

# Casos borde detectados mediante IA

Después del code review se solicitó a la IA una segunda revisión enfocada
exclusivamente en casos borde que no estuvieran cubiertos por los tests
existentes.

La IA identificó varios casos potenciales:

* Sensor inexistente.
* Temperatura exactamente en el cero absoluto.
* Humedad en 0 y 100.
* Presión en 0.
* Valor exactamente igual al umbral.
* Valor ligeramente superior al umbral.
* Unidades inválidas.
* Actualizaciones parciales.
* Lecturas inexistentes.
* Paginación y filtros de fecha.

Se seleccionaron cinco casos para incorporar al pipeline:

1. Sensor inexistente.
2. Temperatura exactamente en `-273.15 °C`.
3. Valor exactamente igual al umbral.
4. Valor ligeramente superior al umbral.
5. Unidad inválida.

Estos casos fueron implementados como cinco tests nuevos en
`tests/test_reading_service.py`.

Durante la ejecución se encontraron dos errores en el código generado por
la IA:

* La IA intentó acceder a `service.notifier`, atributo que no existe
  públicamente en `ReadingService`.
* El test de unidad inválida utilizaba un patrón de texto que no coincidía
  con el mensaje real de la excepción.

Ambos problemas fueron corregidos manualmente.

## Resultado de las pruebas

Después de corregir los tests generados por la IA:

```text
82 passed
Coverage: 92.22%
```

También se ejecutó:

```text
ruff check app tests
All checks passed!

ruff check .
All checks passed!
```

La cobertura final de `92.22%` supera el mínimo requerido de `80%`.

---

# Conclusión

La IA permitió identificar posibles problemas de diseño y varios casos borde
que no estaban cubiertos por los tests existentes.

Sin embargo, no todos los hallazgos requerían modificaciones y algunos
fueron considerados mejoras futuras en lugar de defectos.

Además, los tests generados por la IA requirieron revisión manual antes de
integrarse, ya que dos de ellos contenían errores.

La revisión demuestra que la IA puede acelerar el proceso de code review y
generación de pruebas, pero sus propuestas deben ser verificadas contra el
código real, los contratos existentes, la arquitectura y los resultados del
pipeline.

