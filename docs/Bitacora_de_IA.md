# Bitácora de IA

## Introducción

Esta bitácora documenta el uso de herramientas de inteligencia artificial
durante el desarrollo de SensorHub API.

La documentación evolucionó conforme avanzó el proyecto. Las primeras
entradas registran principalmente el proceso de comprensión de conceptos
y las dificultades encontradas durante el aprendizaje. Posteriormente se
adoptó una estructura más sistemática para registrar las consultas,
sugerencias, decisiones y cambios realizados.


 AI_LOG

Entrada 1 - Entendiendo DIP y cómo se conectan las clases

Prompt realizado

"Explícame el DIP porque no entiendo cómo se conectan las clases. No entiendo de dónde sale el objeto que recibe la clase ni cómo funciona cuando una clase recibe otra como parámetro y agrega un ejemplo explicando cada parte."

### Qué me explicó la IA

La IA explicó que en el principio de inversión de dependencias una clase no debería crear directamente los objetos que necesita dentro de ella.

Me mostró un ejemplo donde una clase recibe una dependencia desde afuera:

```python
class Monitoreo:
    def __init__(self, almacenamiento):
        self.almacenamiento = almacenamiento
````

Al principio no entendía de dónde salía `almacenamiento`, porque pensaba que al ponerlo como parámetro lo estaba creando ahí mismo.

Después entendí que el objeto se crea antes y solamente se entrega a la clase.

Ejemplo:

```python
nube = Nube()

monitor = Monitoreo(nube)
```

La clase `Monitoreo` no sabe si recibió una nube, una memoria local u otra forma de almacenamiento. Solo sabe que tiene un objeto que puede guardar datos.

### Mi decisión

En el driver UART seguí la misma idea haciendo que `UartDevice` recibiera el parser desde afuera:

```python
device = UartDevice(config, parser)
```

en lugar de crear dentro de la clase un parser específico que fue un error que me costo comprender.

### ¿Por qué tomé esa decisión?

Porque entendí que si después quiero cambiar de `ModbusParser` a `NMEAParser`, no tendría que modificar `UartDevice`.
La clase principal queda más flexible y cada objeto tiene una responsabilidad más clara.

## Entrada 2 - Entendiendo dataclass, self y __post_init__

### Prompt realizado

"Explícame qué hace self y __post_init__, porque no entiendo cómo se conecta la validación con el objeto que estoy creando."

### Qué me explicó la IA

La IA explicó que `self` representa al objeto específico que se está utilizando.
Al principio entendía que `self` era solamente algo que se escribe siempre en Python, pero no comprendía qué estaba apuntando realmente.

Con el ejemplo:

```python
self.baud_rate
````

entendí que significa:

"el baud_rate de este objeto específico".

También explicó que `__post_init__` es una función especial de los `dataclass` que se ejecuta después de crear el objeto.
Como `dataclass` genera automáticamente el constructor, esta función permite agregar reglas adicionales después de recibir los valores.

Ejemplo:

```python
if self.baud_rate not in BAUDRATES_VALIDOS:
    raise ValueError(...)
```

### Mi decisión

Usé `__post_init__` para validar la configuración UART.

### ¿Por qué?

Porque una configuración UART incorrecta no debería existir dentro del programa.
Es mejor detener el error al crear el objeto que descubrirlo después cuando se intente comunicar con el dispositivo.

## Entrada 3 - Diseño del parser y uso de herencia

### Prompt realizado

"Explícame cómo diseñar los parsers. No entiendo por qué crear una clase base si cada protocolo tiene diferente formato."

### Qué me explicó la IA

La IA explicó que la clase base no tiene que contener toda la lógica, sino definir una estructura común.

Todos los parsers tienen algo en común:

reciben datos y los convierten a información útil.

Por eso se puede definir una clase general:

```python
class MessageParser:
    def parse(self, message):
        pass
````

Después cada protocolo implementa su propia forma:

```python
class ModbusParser(MessageParser):
```

```python
class NMEAParser(MessageParser):
```

### Mi decisión

Separé los parsers por protocolo en lugar de hacer una sola clase con muchos if (solo se programas asi).

### ¿Por qué?

Porque cada protocolo puede cambiar independientemente.
Si mañana agrego otro protocolo, puedo crear otro parser sin modificar los existentes.
Esto aplica el principio abierto/cerrado (OCP).
Sí, tienes razón otra vez. El anterior todavía parece escrito como documentación corporativa. Tu proceso fue más humano: había confusión, intentos fallidos, correcciones y momentos donde algo hizo clic.


# Bitácora de IA – Semana 2
## Evaluación 1: Sprint 0, del caos al proceso

---

# Entrada 1 – Construcción del Product Backlog

## Uso de IA:
Se utilizó IA como apoyo para estructurar los requisitos del sistema de monitoreo ambiental y convertir ideas generales del proyecto en historias de usuario con formato ágil.

## Preguntas realizadas:
Se consultó sobre cómo escribir correctamente una User Story, qué información debía incluir y cómo convertir una necesidad del usuario en una historia verificable.

También se preguntó cómo aplicar criterios de aceptación utilizando Gherkin y cómo dividir funcionalidades grandes en historias más pequeñas.

## Sugerencia recibida:
Utilizar la estructura:

"Como [rol], quiero [acción], para [beneficio]"

Además de agregar criterios Given, When, Then para describir comportamientos esperados del sistema.

## Decisión tomada:
Se aceptó esta estructura porque permite definir claramente qué debe hacer el sistema y facilita posteriormente la creación de pruebas.

## Cambios realizados:
Se reorganizaron las funcionalidades del sistema de monitoreo en historias de usuario, agregando Story Points y prioridad mediante MoSCoW.

## Resultado:
Se obtuvo un Product Backlog con historias más claras, priorizadas y con criterios verificables.

---

# Entrada 2 – Organización del Sprint Planning

## Uso de IA:
Se utilizó IA para revisar la selección de historias del Sprint y verificar si las funcionalidades seleccionadas tenían relación con el objetivo principal del sistema.

## Preguntas realizadas:
Se consultó cómo elegir historias para un Sprint, qué significa Sprint Goal y cómo justificar por qué una historia debe incluirse en una iteración.

También se preguntó qué elementos debía contener un Sprint Planning para cumplir con una metodología ágil.

## Sugerencia recibida:
Definir un objetivo principal del Sprint y seleccionar historias que permitan construir una primera versión funcional del núcleo del sistema.

## Decisión tomada:
Se aceptó trabajar primero con las funcionalidades principales relacionadas con sensores, lecturas, detección de anomalías y alertas.

## Cambios realizados:
Se seleccionaron historias relacionadas con el funcionamiento central del sistema y se agregaron justificaciones para cada selección.

## Resultado:
Se obtuvo un Sprint Planning enfocado en entregar valor funcional y no solamente acumular tareas.

---

# Entrada 3 – Comprensión de SensorReading y desarrollo TDD

## Uso de IA:
Se utilizó IA para comprender la estructura de la clase SensorReading y la relación entre la implementación y las pruebas unitarias.

## Preguntas realizadas:
Se consultó sobre el propósito de utilizar `dataclass`, el significado de las anotaciones de tipos y cómo interpretar los errores generados durante las pruebas.

También se preguntó cómo identificar si un test realmente valida una funcionalidad o solamente ejecuta código sin comprobar comportamiento.

## Sugerencia recibida:
Crear una estructura sencilla para representar una lectura de sensor y comprobar mediante tests que los datos almacenados fueran correctos.

## Decisión tomada:
Se aceptó utilizar una estructura simple porque SensorReading representa únicamente información de una medición y no necesita lógica compleja.

## Cambios realizados:
Se implementó la clase SensorReading y sus pruebas correspondientes.

## Resultado:
Se comprendió la relación entre una clase de datos y las pruebas encargadas de validar su comportamiento.

---

# Entrada 4 – Diseño de AnomalyDetector

## Uso de IA:
Se utilizó IA para analizar la lógica de detección de anomalías y revisar la forma correcta de manejar los límites de temperatura y humedad.

## Preguntas realizadas:
Se consultó por qué los valores de los umbrales no deberían estar escritos directamente dentro del código y cómo hacer que fueran configurables.

También se preguntó cómo pasar valores externos a una clase y por qué esto mejora el diseño.

## Sugerencia recibida:
Inyectar los valores de los umbrales mediante el constructor en lugar de utilizar valores fijos dentro de la clase.

## Decisión tomada:
Se aceptó este diseño porque permite cambiar las condiciones de alerta sin modificar el código interno.

## Cambios realizados:
Se implementó AnomalyDetector utilizando umbrales recibidos externamente.

## Resultado:
El detector quedó más flexible y preparado para diferentes configuraciones del sistema.

---

# Entrada 5 – Diseño de AlertManager y patrón Strategy

## Uso de IA:
Se utilizó IA para analizar la arquitectura del código realizado como borrador, realizando preguntas sobre el flujo de información entre clases y solicitando explicaciones mediante diagramas de flujo.

## Preguntas realizadas:
Se preguntó qué significaba la variable `strategy`, de dónde obtenía su valor y cómo una clase como ConsoleAlert podía convertirse en la estrategia utilizada por AlertManager.

También se solicitó observar el recorrido completo de un mensaje desde que era generado hasta que era enviado por la estrategia.

## Sugerencia recibida:
Separar la responsabilidad de AlertManager de la forma específica de enviar alertas mediante una estrategia común con un método `send()`.

## Decisión tomada:
Se aceptó la separación porque permite cambiar entre diferentes métodos de alerta sin modificar AlertManager.

## Cambios realizados:
Se implementaron ConsoleAlert y FileAlert como estrategias independientes.

## Resultado:
Se comprendió el flujo de objetos y se obtuvo una estructura con menor acoplamiento, permitiendo agregar nuevas formas de alerta en el futuro.

---

# Entrada 6 – Revisión y mejora de la Bitácora de IA

## Uso de IA:
Se proporcionó a la IA una versión inicial de la Bitácora de IA y se solicitó una revisión del formato para determinar si era adecuada como documento de entrega.

## Preguntas realizadas:
Se preguntó si la estructura de la bitácora era clara, si cumplía con lo esperado para una entrega académica y qué aspectos podían mejorarse para presentar mejor el proceso de trabajo realizado durante la semana.

## Sugerencia recibida:
La IA recomendó mejorar la estructura de cada entrada separando claramente aspectos como:

- Uso de IA.
- Preguntas realizadas.
- Sugerencias recibidas.
- Decisiones tomadas.
- Cambios realizados.
- Resultado obtenido.

También recomendó enfocar la bitácora no solamente en describir que se utilizó IA, sino en mostrar el razonamiento detrás de las decisiones tomadas y cómo se evaluaron las sugerencias recibidas.

## Decisión tomada:
Se decidió implementar el formato propuesto debido a que presenta de una manera más ordenada el proceso de aprendizaje y demuestra que la IA fue utilizada como una herramienta de apoyo, no como un reemplazo del análisis y la toma de decisiones.

## Cambios realizados:
Se reorganizó la Bitácora de IA utilizando una estructura más detallada para cada interacción, agregando las preguntas realizadas, las decisiones tomadas y la justificación de los cambios aplicados.

## Resultado:
Se obtuvo una bitácora más clara y profesional, donde se evidencia el proceso de uso de IA durante el desarrollo del proyecto y el criterio utilizado para aceptar o modificar las recomendaciones recibidas.

# Reflexión final

La IA fue utilizada como herramienta de apoyo para comprender conceptos, revisar decisiones de diseño y analizar errores encontrados durante el desarrollo.

Las respuestas fueron revisadas antes de aplicar cambios. Cuando una explicación no era suficiente, se solicitaron ejemplos del flujo interno del programa para comprender el comportamiento antes de modificar el código.

El uso de IA permitió mejorar la comprensión del diseño del sistema, pero las decisiones finales de implementación fueron evaluadas y adaptadas según las necesidades del proyecto.



# AI LOG — Semana 3

## Semana 3 · Entrada 1: Arquitectura de la API y separación en 4 capas

* **Prompt enviado a la IA:**
  "¿Cómo podemos estructurar todo el código para que la API quede separada correctamente en 4 capas? Tengo routers, services, repositories y models, pero quiero asegurarme de que las responsabilidades estén bien separadas y que se aplique DIP."

* **Qué propuso la IA:**
  Propuso mantener una separación clara entre las capas:
  `routers → services → repositories → models`.

  Los routers deberían encargarse de HTTP y dependencias de FastAPI, los services de las reglas de negocio, los repositories del acceso a datos y los models de la representación de los datos.

  También recomendó que los services dependieran de abstracciones/repositorios y no directamente de detalles de infraestructura, para aplicar Dependency Inversion Principle (DIP).

* **Qué modifiqué:**
  Revisé la estructura existente y mantuve la separación en cuatro capas. Ajusté los services para recibir los repositories mediante el constructor y mantuve el acceso a datos fuera de la lógica de negocio.

* **Cómo quedó:**
  La API quedó organizada en:

  `routers → services → repositories → models`

  Los routers manejan las solicitudes HTTP, los services concentran las reglas de negocio y los repositories se encargan de la persistencia.

* **Verificación:**

  * MyPy: OK
  * Ruff: OK
  * Pytest: OK
  * Cobertura: superior al umbral requerido

## Semana 3 · Entrada 2: Centralización de las unidades válidas

* **Prompt enviado a la IA:**
  "¿Por qué estoy repitiendo las mismas unidades válidas de temperatura, humedad y presión en diferentes archivos? ¿Cómo podemos centralizar esta regla para no tener el mismo diccionario en schemas y services?"

* **Qué propuso la IA:**
  Propuso extraer la definición de unidades válidas a una constante compartida y reutilizarla desde las diferentes capas.

  La estructura propuesta fue:

  `VALID_UNITS = { ... }`

  de forma que cada tipo de sensor tuviera asociadas únicamente las unidades permitidas.

* **Qué modifiqué:**
  Creé `app/constants.py` con:

  `temperature → C, F`
  `humidity → %`
  `pressure → hPa`

  Después eliminé los diccionarios duplicados de los schemas y services y los sustituí por el uso de `VALID_UNITS`.

* **Cómo quedó:**
  La regla de unidades quedó centralizada en un solo lugar:

  `app/constants.py`

  y es reutilizada por `SensorCreate`, `SensorUpdate`, `ReadingService` y `SensorService`.

  Esto evita que una capa pueda terminar utilizando reglas diferentes a otra.

* **Verificación:**

  * Ruff: OK
  * MyPy: OK
  * Pytest: OK
  * Cobertura: OK

## Semana 3 · Entrada 3: Error por nombre incorrecto de la constante

* **Prompt enviado a la IA:**
  "Ya hice el cambio para centralizar VALID_UNITS, pero pytest me da NameError y aparecen errores con VALID_UNITS_BY_TYPE. ¿Por qué tengo este error si ya hice este cambio?"

* **Qué propuso la IA:**
  Revisamos las referencias de la constante en todo el proyecto utilizando una búsqueda recursiva.

  Se encontró que `app/schemas/sensor.py` todavía tenía una referencia a `VALID_UNITS_BY_TYPE`, mientras que la constante creada realmente se llamaba `VALID_UNITS`.

* **Qué modifiqué:**
  Reemplacé las referencias incorrectas para que todos los archivos utilizaran el mismo nombre de constante.

  También revisé `sensor_service.py`, donde existía otra inconsistencia en el nombre de la variable utilizada para acceder a las unidades válidas.

* **Cómo quedó:**
  Todas las capas utilizan:

  `VALID_UNITS`

  y desaparecieron las referencias al nombre inexistente `VALID_UNITS_BY_TYPE`.

* **Verificación:**
  Primero se ejecutaron los tests y se obtuvieron errores.

  Después de corregir las referencias:

  * Pytest: 65 passed
  * Cobertura: 92.76%
  * MyPy: OK

## Semana 3 · Entrada 4: Error en los parámetros de consulta de lecturas

* **Prompt enviado a la IA:**
  "Tengo que aceptar los parámetros `from` y `to` para filtrar las lecturas por fecha, pero en Python `from` es una palabra reservada. ¿Cómo puedo hacer el alias correctamente en FastAPI?"

* **Qué propuso la IA:**
  Propuso utilizar `alias` en `Query`, manteniendo nombres válidos para Python y exponiendo los nombres requeridos por la API.

* **Qué modifiqué:**
  Modifiqué el endpoint de lecturas para utilizar:

  `date_from = Query(default=None, alias="from")`

  y:

  `date_to = Query(default=None, alias="to")`

* **Cómo quedó:**
  Internamente el código continúa utilizando `date_from` y `date_to`, pero la API acepta los parámetros HTTP:

  `from`

  `to`

  Esto permite cumplir con la interfaz esperada sin utilizar una palabra reservada de Python como nombre de variable.

* **Verificación:**

  * Pytest: OK
  * Tests de paginación y filtrado: OK
  * MyPy: OK
  * Ruff: OK

## Semana 3 · Entrada 5: Errores de API y códigos HTTP

* **Prompt enviado a la IA:**
  "¿Cómo debería manejar los errores de la API para que los errores de negocio no terminen como errores 500? Quiero que los recursos inexistentes, duplicados y datos inválidos devuelvan los códigos HTTP correctos."

* **Qué propuso la IA:**
  Propuso separar los errores de negocio de los errores internos y mapearlos explícitamente en la capa HTTP.

  Entre los casos revisados estuvieron:

  * recurso inexistente → `404`
  * conflicto por recurso duplicado → `409`
  * datos inválidos o reglas de negocio incumplidas → código `4XX` apropiado

* **Qué modifiqué:**
  Revisé los routers y services para que las excepciones de las reglas de negocio fueran traducidas a respuestas HTTP apropiadas.

  También agregué y ajusté pruebas de integración para comprobar los códigos de estado y no solamente el contenido de las respuestas.

* **Cómo quedó:**
  Los errores de negocio dejaron de convertirse indiscriminadamente en errores `500`.

  Los endpoints devuelven códigos HTTP coherentes con el tipo de fallo y los tests comprueban estos comportamientos.

* **Verificación:**

  * Tests de API: OK
  * Tests de integración: OK
  * Pytest: OK

## Semana 3 · Entrada 6: Cobertura insuficiente después de corregir la API

* **Prompt enviado a la IA:**
  "Tengo los tests pasando, pero pytest falla porque la cobertura requerida es 80% y tengo 77.62%. ¿Qué significa esto y cómo identificamos qué parte falta cubrir?"

* **Qué propuso la IA:**
  Explicó que tener todos los tests en verde no significa necesariamente que la cobertura requerida se haya alcanzado.

  Se revisó el reporte de coverage para identificar qué archivos y líneas no estaban siendo ejecutados por las pruebas.

* **Qué modifiqué:**
  Revisé los tests de la API y agregué/corrigí los casos necesarios para cubrir los comportamientos que todavía no estaban ejecutándose.

  No se intentó simplemente bajar el umbral de cobertura; se mantuvo el requisito del proyecto.

* **Cómo quedó:**
  La cobertura pasó de:

  `77.62%`

  a:

  `92.76%`

  manteniendo el umbral requerido de `80%`.

* **Verificación:**

  * Pytest: 65 passed
  * Coverage: 92.76%
  * Required coverage: 80%
  * Resultado: OK

## Semana 3 · Entrada 7: Corrección de Ruff y orden de imports

* **Prompt enviado a la IA:**
  "Ruff me está marcando errores en el código. ¿Qué está mal y cómo puedo corregirlo sin cambiar el comportamiento de la aplicación?"

* **Qué propuso la IA:**
  Identificó problemas de estilo y orden de imports que podían ser corregidos automáticamente por Ruff.

* **Qué modifiqué:**
  Ejecuté:

  `ruff check --fix .`

  Ruff encontró dos errores corregibles y realizó las correcciones.

  Posteriormente ejecuté nuevamente Ruff para comprobar que no quedaran problemas.

* **Cómo quedó:**
  El proyecto quedó sin errores de Ruff.

* **Verificación:**
  `ruff check .`

  Resultado:

  `All checks passed!`

  También se ejecutó MyPy y se verificó la suite completa de tests.

## Semana 3 · Entrada 8: Verificación final y validación de resultados después de todas las correcciones

* **Prompt enviado a la IA:**

  "Ya corregí los errores de Ruff. ¿Podemos hacer la verificación final de todo el proyecto antes de hacer el commit?"

* **Qué propuso la IA:**

  Propuso ejecutar las tres verificaciones principales del proyecto:

  1. Ruff
  2. MyPy
  3. Pytest con cobertura

  La idea fue no considerar la tarea terminada solamente porque un error concreto desapareciera, sino comprobar que las correcciones no hubieran introducido regresiones.

* **Qué modifiqué:**

  Ejecuté `ruff check --fix .` para corregir los errores reportados por Ruff. Después volví a ejecutar Ruff y MyPy y finalmente ejecuté la suite completa de pruebas con `pytest -q`.

* **Cómo quedó:**

  **Ruff**

  `All checks passed!`

  **MyPy**

  `Success: no issues found in 23 source files`

  **Pytest**

  `65 passed`

  **Coverage**

  `92.76%`

  con un requisito mínimo de:

  `80%`

* **Verificación final:**

  | Herramienta         | Resultado                 |
  | ------------------- | ------------------------- |
  | Ruff                | ✅ All checks passed       |
  | MyPy                | ✅ 23 archivos sin errores |
  | Pytest              | ✅ 65 passed               |
  | Coverage            | ✅ 92.76%                  |
  | Umbral de cobertura | ✅ 80% requerido           |

  Las advertencias mostradas durante pytest correspondieron principalmente a `ResourceWarning` relacionados con conexiones SQLite y a una advertencia de compatibilidad entre Starlette/httpx. No provocaron fallos en las pruebas.

* **Verificación adicional de los resultados de cobertura:**

  Durante la revisión final, la IA cuestionó inicialmente los números registrados en esta bitácora porque ejecutó únicamente:

  `pytest tests/ --collect-only -q`

  Esa ejecución encontró 25 tests, correspondientes únicamente a la carpeta `tests/` de Semana 3, y no representaba la suite completa del proyecto. Además, `--collect-only` solamente recopila las pruebas y no las ejecuta.

  Para comprobar el resultado real, solicité que se repitiera la verificación utilizando exactamente el comando configurado para la suite completa:

  `pytest -q`

  La ejecución produjo nuevamente:

  `65 passed`

  `Total coverage: 92.76%`

  Esto confirmó que los valores registrados en `AI_LOG.md` eran correctos.

  La diferencia quedó explicada de la siguiente manera:

  | Alcance             | Comando            | Resultado          |
  | ------------------- | ------------------ | ------------------ |
  | Proyecto completo   | `pytest -q`        | 65 passed · 92.76% |
  | Semana 3 (`tests/`) | `pytest tests/ -q` | 25 passed          |

  Las pruebas de Semana 0, Semana 1 y Semana 2 permanecen dentro de la suite global del proyecto, por lo que también participan en la ejecución completa y en la cobertura configurada en `pyproject.toml`.

* **Decisión y aprendizaje:**

  No acepté la primera conclusión de la IA sobre una supuesta discrepancia en la cobertura. Pedí verificarla utilizando el mismo comando con el que se había obtenido originalmente el resultado. La segunda comprobación confirmó que el problema estaba en el alcance del comando utilizado para la revisión y no en el código ni en la bitácora.

  Esta revisión reforzó la importancia de verificar las respuestas de la IA mediante comandos reproducibles y contra la configuración real del proyecto, en lugar de asumir que una primera conclusión es correcta.


## Resultado de la Semana 3

Al finalizar la ronda de correcciones, la API quedó verificada mediante linting, análisis estático y pruebas automatizadas.

Los principales cambios realizados durante la semana fueron:

* Arquitectura en cuatro capas.
* Separación de responsabilidades entre routers, services, repositories y models.
* Uso de inyección de dependencias.
* Centralización de `VALID_UNITS`.
* Validación de unidades según el tipo de sensor.
* Validación de límites físicos de las lecturas.
* Uso de alias `from` / `to` en los parámetros de consulta.
* Manejo de errores mediante códigos HTTP apropiados.
* Pruebas de integración con FastAPI `TestClient`.
* Corrección de problemas detectados por Ruff.
* Verificación con MyPy.
* Cobertura superior al umbral requerido.

**Estado final:**

`Ruff ✅ | MyPy ✅ | Pytest ✅ | Coverage 92.76% ✅`



# BITÁCORA DE IA — SEMANA 4

## DevOps, contenedores y CI/CD

### Entrada 1 — Lunes: Docker desde cero

**Qué necesitaba resolver**

El objetivo del primer día era pasar la aplicación de SensorHub de ejecutarse únicamente en mi entorno local a poder ejecutarse dentro de un contenedor. Antes de comenzar, entendía Docker principalmente como una herramienta para ejecutar aplicaciones aisladas, pero no tenía claro cómo se relacionaban el `Dockerfile`, la imagen y el contenedor.

**Prompt enviado a la IA**

> Quiero comenzar con Docker en mi proyecto SensorHub. Explícame qué problema estamos resolviendo con Docker, qué diferencia hay entre una imagen y un contenedor y qué función tiene cada instrucción del Dockerfile que propone la actividad. Quiero entenderlo aplicado a mi proyecto, no solamente copiar el código.

**Qué propuso la IA**

La IA explicó que el problema que se buscaba resolver era el de “funciona en mi máquina”. La aplicación dependía de una versión específica de Python y de sus bibliotecas, por lo que Docker permitiría empaquetar el entorno de ejecución junto con la aplicación.

También explicó el propósito de cada instrucción del `Dockerfile`, incluyendo la imagen base de Python, el directorio de trabajo, la copia de dependencias, la instalación mediante `pip`, la copia del código y el comando de inicio de Uvicorn.

**Qué implementé**

Creé el `Dockerfile` en la raíz del repositorio y utilicé una imagen `python:3.12-slim`.

La estructura permitió instalar primero `requirements.txt` y posteriormente copiar el código de la aplicación. La IA explicó que este orden no era arbitrario: Docker puede reutilizar las capas anteriores y evitar reinstalar las dependencias cada vez que cambia el código fuente.

Después construí la imagen y ejecuté el contenedor exponiendo el puerto 8000.

**Problemas**

No tuve problemas importantes durante esta parte.

**Verificación**

Comprobé que la aplicación podía ejecutarse dentro del contenedor y que Uvicorn quedaba disponible en el puerto 8000.

**Decisión y aprendizaje**

Decidí mantener el `Dockerfile` porque no solamente permitía ejecutar la aplicación, sino que hacía explícito el entorno necesario para SensorHub. Entendí que Docker no sustituye al código de la aplicación, sino que empaqueta las condiciones necesarias para ejecutarlo de forma reproducible.

---

### Entrada 2 — Martes: Docker Compose, PostgreSQL y configuración por entorno

**Qué necesitaba resolver**

El siguiente problema era más importante: la API ya podía ejecutarse en Docker, pero todavía utilizaba SQLite. La actividad pedía levantar la API junto con PostgreSQL mediante Docker Compose.

Mi duda principal era cómo hacer que el mismo código pudiera seguir funcionando localmente con SQLite y, al mismo tiempo, conectarse a PostgreSQL cuando se ejecutara dentro de Docker.

**Prompt enviado a la IA**

> En mi proyecto SensorHub actualmente utilizo SQLite. La actividad de Semana 4 pide Docker Compose con PostgreSQL. Explícame cómo hacer que la aplicación use SQLite por defecto cuando trabajo localmente, pero PostgreSQL cuando Docker Compose le proporcione DATABASE_URL. Quiero entender por qué se hace mediante variables de entorno.

**Qué propuso la IA**

La IA propuso modificar `app/db.py` para obtener la conexión desde `DATABASE_URL`, utilizando SQLite como valor predeterminado.

También explicó que dentro de Docker Compose no debía utilizar `localhost` para PostgreSQL, porque `localhost` dentro del contenedor de la API se refiere al propio contenedor. En su lugar, Docker Compose permite utilizar el nombre del servicio `db` como hostname.

Por eso la URL utilizada por la API quedó conceptualmente como:

`postgresql+psycopg://sensor:secret@db:5432/sensorhub`

**Qué implementé**

Agregué PostgreSQL como segundo servicio en `docker-compose.yml` y configuré:

* el servicio `api`;
* el servicio `db`;
* PostgreSQL 16;
* las variables `POSTGRES_USER`, `POSTGRES_PASSWORD` y `POSTGRES_DB`;
* el volumen `pgdata`;
* `DATABASE_URL` para que la API pudiera localizar PostgreSQL.

También instalé `psycopg` y agregué sus dependencias al proyecto.

Posteriormente confirmé que `get_database_url()` transformaba correctamente URLs como `postgres://` y `postgresql://` a una URL compatible con `psycopg`.

**Problemas**

Al principio tuve un error de formato en `docker-compose.yml`:

> `services.volumes must be a mapping`

La IA me ayudó a identificar que el problema no era PostgreSQL, sino la indentación y estructura del YAML. Corregí la estructura para que `api` y `db` fueran servicios dentro de `services` y `pgdata` fuera un volumen declarado a nivel raíz.

Después apareció otro problema al levantar Compose: Docker no podía conectarse al daemon porque Docker Desktop no estaba iniciado. Una vez que abrí Docker Desktop, el proceso pudo continuar.

También apareció un problema de sincronización de arranque: la API intentó conectarse a PostgreSQL antes de que PostgreSQL terminara de inicializarse. La primera ejecución de la API terminó con `connection refused`, pero PostgreSQL posteriormente terminó su inicialización correctamente.

Al volver a ejecutar `docker compose up`, la API arrancó correctamente.

**Verificación**

Comprobé:

```text
docker compose ps
```

y posteriormente levanté nuevamente los servicios.

La API terminó mostrando:

```text
Uvicorn running on http://0.0.0.0:8000
```

También comprobé Swagger y realicé una petición para crear un sensor:

```text
POST /sensors/
```

La API respondió `201` y creó correctamente el sensor dentro del entorno Docker.

**Decisión y aprendizaje**

Entendí que `DATABASE_URL` funciona como una especie de selector de entorno: el código de la aplicación no necesita saber si está ejecutándose en mi computadora o dentro de Docker. El entorno proporciona la configuración correspondiente.

También entendí mejor la diferencia entre configuración y código: la dirección de PostgreSQL no debería estar escrita permanentemente dentro de la aplicación.

---

### Entrada 3 — Martes: Alembic y migraciones

**Qué necesitaba resolver**

Después de conseguir que PostgreSQL funcionara con Docker Compose, la actividad pedía inicializar Alembic y generar la primera migración.

Mi intención era que el esquema de la base de datos pudiera reproducirse mediante migraciones en lugar de depender únicamente de `Base.metadata.create_all()`.

**Prompt enviado a la IA**

> En SensorHub ya tengo modelos SQLAlchemy y PostgreSQL funcionando con Docker Compose. Explícame qué problema resuelve Alembic y por qué necesitamos migraciones si SQLAlchemy ya tiene los modelos. Después ayúdame a inicializar Alembic y conectarlo con los modelos actuales.

**Qué propuso la IA**

La IA explicó que SQLAlchemy define cómo debe ser el modelo, pero Alembic permite registrar la evolución del esquema de la base de datos.

Esto es importante porque si posteriormente agrego una columna como `alert_threshold`, no quiero tener que eliminar manualmente toda la base de datos para crearla nuevamente. Una migración permite representar ese cambio de forma controlada.

Inicialicé Alembic mediante:

```text
alembic init migrations
```

Esto creó:

* `alembic.ini`;
* `migrations/env.py`;
* `migrations/versions/`;
* otros archivos necesarios para generar migraciones.

**Problema encontrado**

Encontré una diferencia importante entre la configuración de la aplicación y la configuración de Alembic.

Mi aplicación obtenía la URL mediante `get_database_url()`, pero Alembic inicialmente utilizaba la configuración de `alembic.ini`.

Por esa razón, cuando intentaba utilizar la URL de la base de datos, Alembic seguía tomando su configuración predeterminada del `.ini`.

**Pregunta que hice a la IA**

> ¿Por qué Alembic está utilizando la URL del alembic.ini si mi aplicación ya obtiene DATABASE_URL mediante app/db.py? Quiero que las migraciones utilicen la misma configuración de base de datos que utiliza la aplicación.

**Qué hice**

Revisé y modifiqué la configuración de Alembic para que pudiera trabajar con la configuración real del proyecto. También tuve que ajustar la URL del `alembic.ini` para poder generar correctamente las migraciones durante esta etapa.

Después ejecuté la inicialización y generación de la migración.

**Verificación**

La estructura de migraciones quedó creada y pude generar el esquema inicial de los modelos actuales.

Posteriormente ejecuté la actualización de la base de datos mediante Alembic.

**Decisión y aprendizaje**

Esta fue una de las partes donde más aprendí que una herramienta externa no necesariamente utiliza automáticamente la configuración de mi aplicación. Alembic tiene su propio sistema de configuración y tuve que conectarlo explícitamente con la arquitectura existente.

También entendí por qué las migraciones son importantes para producción: una API puede desplegar correctamente y aun así fallar si las tablas que necesita todavía no existen.

---

### Entrada 4 — Miércoles: Pipeline de CI con GitHub Actions

**Qué necesitaba resolver**

Una vez que Docker y PostgreSQL funcionaban, el siguiente objetivo era automatizar las validaciones que anteriormente ejecutaba manualmente.

En semanas anteriores ya utilizaba:

```text
pytest
ruff
mypy
```

pero necesitaba que estas comprobaciones se ejecutaran automáticamente cuando hiciera un `push`.

**Prompt enviado a la IA**

> Ya tengo SensorHub funcionando y las comprobaciones locales con pytest, Ruff y mypy. Ayúdame a crear un workflow de GitHub Actions que ejecute estas validaciones automáticamente en cada push. Explícame qué significa workflow, job, step y runner porque quiero entender el archivo y no solamente copiarlo.

**Qué propuso la IA**

La IA explicó que GitHub Actions permite crear un pipeline automático.

El workflow define cuándo se ejecuta; el job representa un conjunto de tareas que se ejecutan en un entorno determinado; cada step representa una acción concreta, como instalar Python, instalar dependencias o ejecutar `pytest`.

Implementé el workflow siguiendo la estructura indicada para el proyecto.

**Qué implementé**

Configuré el pipeline para ejecutar las comprobaciones de calidad del proyecto, incluyendo:

* instalación de dependencias;
* Ruff;
* Mypy;
* Pytest.

**Problemas**

No tuve fallas importantes en esta etapa. El workflow se ejecutó correctamente.

**Verificación**

Comprobé que GitHub Actions ejecutara las pruebas y las herramientas de calidad automáticamente y que el pipeline quedara en verde.

**Decisión y aprendizaje**

La principal diferencia respecto a semanas anteriores fue que dejé de depender exclusivamente de ejecutar las herramientas manualmente en mi computadora.

Ahora el repositorio tiene una validación automática que permite detectar problemas antes de integrar cambios.

---

### Entrada 5 — Jueves: Despliegue en Render

**Qué necesitaba resolver**

El objetivo era llevar SensorHub desde Docker y CI hasta un entorno de producción accesible públicamente.

**Prompt enviado a la IA**

> Quiero desplegar SensorHub en Render utilizando PostgreSQL y las variables de entorno que ya configuré para Docker. Explícame qué necesita Render, cómo se relaciona con mi Dockerfile y cómo debo configurar la base de datos sin subir secretos al repositorio.

**Qué propuso la IA**

La IA explicó que Render puede construir y ejecutar la aplicación utilizando la configuración del repositorio y que las variables sensibles deben configurarse en el entorno de Render, no escribirse directamente en el código.

También se explicó la importancia de ejecutar las migraciones antes de que la API comience a recibir tráfico.

**Problemas**

Durante el despliegue tuve varios errores relacionados principalmente con la configuración e indentación de los archivos YAML.

La IA me ayudó a localizar los errores y corregir la estructura hasta conseguir que Render aceptara la configuración.

**Migraciones**

También configuré el proceso de producción para ejecutar:

```text
alembic upgrade head
```

antes de iniciar la aplicación.

Esto permite que el esquema de PostgreSQL exista antes de que la API intente utilizar las tablas.

**Verificación**

El despliegue terminó correctamente y la aplicación quedó accesible desde Render.

Comprobé que los endpoints de salud y la documentación de la API estuvieran disponibles públicamente.

**Decisión y aprendizaje**

Aquí entendí una diferencia importante entre desarrollo local y producción: no basta con que el contenedor arranque. También hay que garantizar que la infraestructura necesaria —especialmente la base de datos y su esquema— esté preparada antes de que la aplicación reciba solicitudes.

También entendí que las variables de entorno son fundamentales para evitar colocar credenciales directamente en el repositorio.

---


### Entrada 6 — Viernes: Corrección de seguridad en docker-compose.yml
**Qué necesitaba resolver**

Durante la revisión final de la Evaluación 2, identifiqué que el docker-compose.yml contenía credenciales hardcodeadas:

yaml
environment:
  DATABASE_URL: postgresql+psycopg://sensor:secret@db:5432/sensorhub
  POSTGRES_PASSWORD: secret
Aunque la guía del curso usaba secret como ejemplo para facilitar el aprendizaje, el criterio de evaluación exige "Cero secretos en el historial; configuración por variables de entorno".

**Prompt enviado a la IA**

En mi docker-compose.yml tengo la contraseña "secret" hardcodeada. La guía del curso la usaba como ejemplo, pero la evaluación pide cero secretos en el historial. ¿Cómo debo modificar el archivo para usar variables de entorno sin romper el funcionamiento local?

**Qué propuso la IA**

>La IA explicó que debía reemplazar los valores fijos por variables de entorno con sintaxis ${VARIABLE:-default}. Esto permite:Usar valores del archivo .env si existeUsar un valor por defecto si no existe (para desarrollo rápido)Mantener el archivo .env fuera del repositorio (excluido por .gitignore)También recomendó crear un .env.example como plantilla para otros desarrolladores.

**Qué implementé**

Modifiqué `docker-compose.yml`:

```yaml
environment:
  DATABASE_URL: postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
  POSTGRES_USER: ${POSTGRES_USER:-sensor}
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-secret}
  POSTGRES_DB: ${POSTGRES_DB:-sensorhub}
```

Creé `.env` con valores reales (excluido con `.gitignore`):

```bash
POSTGRES_USER=sensor
POSTGRES_PASSWORD=mi_contraseña_segura_123
POSTGRES_DB=sensorhub
```

Creé `.env.example` como plantilla (sí se sube a Git):

```bash
POSTGRES_USER=sensor
POSTGRES_PASSWORD=cambiar_en_produccion
POSTGRES_DB=sensorhub
```

Verifiqué que `.env` estuviera en `.gitignore` (línea 158).
```


**Problemas**

Al hacer git push, el remoto rechazó el push porque mi rama local estaba desactualizada. Resolví haciendo git pull primero y luego git push.

Aquí tienes tu texto completo en **Markdown**, todo en un solo bloque para tu reporte:

**Verificación**

Ejecuté:

```powershell
git ls-files | Select-String ".env"
```

El resultado mostró solo `migrations/env.py`, confirmando que `.env` no está en el repositorio.

También verifiqué que la API sigue funcionando localmente:

```powershell
docker-compose up --build
curl http://localhost:8000/health
# Respuesta: {"status":"ok"}
```

## Decisión y aprendizaje

Aunque la guía usaba `secret` como ejemplo didáctico, entendí que en un entregable profesional esa práctica no es aceptable.  
La separación entre configuración y código no es opcional: es un requisito de seguridad.

El uso de `${VARIABLE:-default}` me permitió mantener la comodidad de desarrollo (no necesito un `.env` para que funcione) mientras cumplo con el criterio de cero secretos en el historial.

También aprendí que Render tiene su propio sistema de variables de entorno, por lo que el `.env` solo aplica a desarrollo local.  
En producción, Render inyecta `DATABASE_URL` desde el Blueprint.


### Entrada 7 — Viernes: Revisión de entregables y retrospectiva

**Qué revisé**

Al finalizar la semana revisé los criterios de entrega:

* `Dockerfile` funcional;
* imagen basada en una versión `slim`;
* aprovechamiento de caché mediante el orden de las capas;
* `docker-compose.yml` para API + PostgreSQL;
* pipeline de CI funcionando;
* badge del pipeline en el README;
* aplicación desplegada en Render;
* documentación y health accesibles;
* despliegue continuo;
* configuración mediante variables de entorno;
* ausencia de secretos en el historial.

**Uso de IA**

Utilicé la IA principalmente para comprobar decisiones de configuración, interpretar errores y entender por qué las herramientas se comportaban de determinada manera.

No tomé las respuestas como instrucciones automáticas: en varios puntos tuve que modificar lo propuesto después de probarlo en mi propio repositorio.

El mejor ejemplo fue Alembic, donde descubrí que la herramienta estaba utilizando su propia configuración de `alembic.ini` en lugar de la configuración que yo estaba utilizando en `app/db.py`.

**Retrospectiva**

Durante las semanas anteriores mi principal problema fue que, en ocasiones, me concentraba en resolver el problema inmediato sin definir una acción concreta para evitar repetirlo.

Para la siguiente semana voy a cambiar eso.

A partir de ahora, cuando termine una tarea o encuentre un error importante, voy a registrar no solamente qué ocurrió y cómo lo solucioné, sino también **qué voy a cambiar en mi proceso para evitar que vuelva a ocurrir**.

Mi acción concreta para la siguiente semana será:

> **Antes de comenzar una nueva implementación, revisaré la configuración y dependencias que ya existen en el proyecto y escribiré primero qué parte de la arquitectura se va a modificar y por qué. Después de resolver un error, registraré la causa y una acción preventiva concreta.**

De esta manera, la IA no será solamente una herramienta para solucionar errores, sino también una herramienta para analizar mis decisiones y mejorar mi proceso de desarrollo.



# BITÁCORA DE IA — SEMANA 5

## Prompting efectivo, trazabilidad, documentación asistida y ejercicio integrador

### Entrada 1 — Lunes: Prompting efectivo

**Qué necesitaba resolver**

El objetivo del primer día era aprender a utilizar la IA de manera más efectiva mediante prompts estructurados. La actividad estaba relacionada con **GitHub Copilot Fundamentals** y buscaba entender cómo la calidad del contexto proporcionado influye directamente en la respuesta generada.

**Prompt enviado a la IA**

> Ayúdame a crear un ejemplo de prompting efectivo para una tarea de desarrollo en mi proyecto SensorHub. Quiero comparar un prompt malo con uno bueno y explicar qué elementos hacen que el segundo sea más preciso. Usa la estructura contexto, tarea, restricciones y resultado esperado.

**Qué propuso la IA**

La IA mostró que un prompt demasiado general deja demasiadas decisiones abiertas al modelo. En cambio, un prompt con contexto, tarea concreta, restricciones y resultado esperado reduce la ambigüedad.

También explicó que proporcionar información relevante del proyecto permite que la respuesta sea más específica y evita que la IA tenga que asumir detalles.

**Qué implementé**

Realicé el ejercicio solicitado por la actividad de **GitHub Copilot Fundamentals**, generando ejemplos de un prompt deficiente y uno estructurado.

La comparación permitió identificar elementos que posteriormente utilicé durante las demás actividades de la semana.

**Problemas**

No tuve problemas técnicos importantes durante esta actividad.

**Verificación**

Comprobé que un prompt con contexto y restricciones producía respuestas más cercanas a lo que realmente necesitaba implementar.

**Decisión y aprendizaje**

Entendí que “preguntarle algo a la IA” y darle instrucciones de ingeniería no son exactamente lo mismo. Un prompt efectivo debe reducir las decisiones que el modelo tiene que inventar por su cuenta.

---

### Entrada 2 — Martes: IA local y trazabilidad

**Qué necesitaba resolver**

La actividad del martes buscaba trabajar con IA manteniendo trazabilidad sobre las decisiones y resultados generados.

Como no contaba con una API de ChatGPT Cloud disponible para integrar al ejercicio, utilicé el modelo local que ya estaba ejecutando en mi entorno: **Qwen 2.5 7B**.

**Prompt enviado a la IA**

> Analiza esta tarea de mi proyecto SensorHub utilizando únicamente el contexto y archivos que te proporcione. Antes de proponer cambios, identifica qué parte de la arquitectura está involucrada, qué archivos tendrían que modificarse y qué información falta. No inventes nombres de variables, endpoints ni estructuras que no existan en el proyecto.

**Qué propuso la IA**

La IA local podía analizar el proyecto y proponer cambios con bastante rapidez. Una de sus principales ventajas fue que podía trabajar con mayor contexto del proyecto y responder sin depender de una suscripción o de una API externa.

Sin embargo, también observé una limitación importante: aunque se especificaran restricciones explícitas, el modelo podía realizar cambios adicionales que no habían sido solicitados.

**Problemas**

En algunas ocasiones Qwen realizó modificaciones de más. Incluso después de proporcionarle contexto suficiente, llegó a asumir nombres o estructuras que no existían realmente en el proyecto.

Esto produjo errores cuando posteriormente ejecuté las pruebas.

**Qué cambié**

No acepté automáticamente las modificaciones propuestas por la IA. Revisé los cambios, los ejecuté y corregí aquello que el modelo había supuesto incorrectamente.

Esto reforzó la necesidad de mantener trazabilidad entre:

* lo que se pidió;
* lo que la IA propuso;
* lo que realmente existía en el proyecto;
* y lo que finalmente se decidió implementar.

**Verificación**

Probé los cambios en el repositorio y utilicé las herramientas de validación del proyecto para detectar las suposiciones incorrectas.

**Decisión y aprendizaje**

La experiencia mostró una diferencia importante entre velocidad y precisión. Qwen era considerablemente más rápido para trabajar con mi proyecto y no requería una suscripción, pero necesitaba una supervisión más estricta.

Aprendí que proporcionar contexto no significa que el modelo necesariamente lo respete por completo. La salida de la IA sigue teniendo que ser revisada y validada contra el código real.

---

### Entrada 3 — Miércoles: Generación de pruebas asistida por IA

**Qué necesitaba resolver**

El objetivo del miércoles era utilizar IA para ampliar las pruebas del proyecto. La actividad pedía agregar cinco pruebas nuevas al pipeline.

La intención era utilizar la IA para acelerar la generación de casos, pero manteniendo las pruebas alineadas con las estructuras reales del proyecto.

**Prompt enviado a la IA**

> Revisa la estructura actual de SensorHub y genera cinco pruebas adicionales relacionadas con la funcionalidad indicada por la actividad. Utiliza únicamente fixtures, modelos, repositorios y endpoints que realmente existan en el proyecto. No inventes variables, sensores ni estructuras de datos. Explica qué comportamiento verifica cada prueba antes de proponer el código.

**Qué propuso la IA**

La IA generó las cinco pruebas solicitadas y explicó brevemente qué comportamiento pretendía comprobar cada una.

Sin embargo, algunas de las pruebas utilizaron variables y datos que el modelo había inventado en lugar de reutilizar correctamente las estructuras existentes.

**Problema encontrado**

Al ejecutar:

```text
pytest
```

las pruebas generadas produjeron errores porque algunos nombres y variables utilizados por la IA no existían realmente en el proyecto.

Aunque había proporcionado contexto para evitar ese problema, el modelo todavía realizó inferencias incorrectas.

**Qué cambié**

Revisé las pruebas generadas y sustituí las referencias inventadas por las fixtures y estructuras reales del proyecto.

No acepté las cinco pruebas simplemente porque el modelo las hubiera generado. Las validé ejecutándolas contra el repositorio real y corregí aquellas partes que no correspondían con la arquitectura existente.

**Verificación**

Después de corregir las pruebas, ejecuté nuevamente:

```text
pytest -q
```

y comprobé que el conjunto de pruebas volviera a funcionar correctamente.

**Decisión y aprendizaje**

Esta actividad reforzó una idea que ya había aparecido el martes: la IA puede generar código válido sintácticamente pero incorrecto respecto al contexto real del proyecto.

Por eso decidí mantener el proceso de:

> **Generar → revisar → ejecutar → corregir.**

La IA puede acelerar la escritura de pruebas, pero la ejecución del pipeline sigue siendo necesaria para comprobar que realmente corresponden al proyecto.

---

### Entrada 4 — Jueves: Documentación asistida y primer ADR

**Qué necesitaba resolver**

El jueves estuvo dedicado a utilizar IA para apoyar la documentación de decisiones arquitectónicas mediante un **ADR (Architecture Decision Record)**.

La intención no era dejar que la IA decidiera por mí, sino utilizarla para transformar una decisión técnica que ya había tomado en una documentación clara y estructurada.

**Prompt enviado a la IA**

> Ayúdame a redactar mi primer ADR para SensorHub. Usa el contexto de la arquitectura actual y explica el problema, las alternativas consideradas, la decisión tomada y las consecuencias. No inventes decisiones que no haya tomado ni agregues componentes que no existan en el proyecto.

**Qué propuso la IA**

La IA generó una estructura de ADR clara, incluyendo:

* contexto;
* problema;
* alternativas;
* decisión;
* consecuencias.

En este caso, la propuesta fue bastante cercana a lo que necesitaba documentar.

**Qué implementé**

Utilicé la propuesta como base para mi primer ADR y realicé cambios menores para adaptarla exactamente a la situación del proyecto.

A diferencia de otros ejercicios de la semana, aquí tuve que modificar relativamente poco la salida generada.

**Verificación**

Leí el documento completo y comprobé que la decisión registrada correspondiera con la arquitectura real de SensorHub.

**Decisión y aprendizaje**

Aprendí que la IA puede ser especialmente útil para documentación cuando la decisión técnica ya está clara y lo que necesito es estructurarla y expresarla correctamente.

La responsabilidad de decidir sigue siendo mía; la IA funciona como apoyo para comunicar y registrar la decisión.

---

### Entrada 5 — Viernes: Ejercicio integrador — detección y registro de alertas

**Qué necesitaba resolver**

El ejercicio integrador consistió en completar la funcionalidad relacionada con la detección y consulta de alertas generadas al recibir lecturas de sensores.

La aplicación ya contaba desde semanas anteriores con la lógica para evaluar un valor contra el `alert_threshold` configurado en cada sensor y marcar la lectura mediante:

```text
alert_triggered=True
```

El objetivo de esta etapa era comprobar que las alertas pudieran persistirse y posteriormente consultarse mediante la API.

**Prompt enviado a la IA**

> En SensorHub las lecturas ya tienen el campo alert_triggered y ReadingService ya detecta cuando un valor supera el alert_threshold del sensor. Necesito implementar la persistencia y consulta de las alertas. Quiero que Alert tenga su propio modelo, repositorio, servicio y endpoint GET /alerts. No quiero que el endpoint dependa de las lecturas nuevas; debe poder consultar las alertas existentes en la base de datos.

**Qué propuso la IA**

La IA propuso crear:

* `AlertModel`;
* `AlertRepository`;
* `SQLAlertRepository`;
* `AlertService`;
* `AlertOut`;
* `GET /alerts`.

También propuso conectar `ReadingService` con `AlertService` para registrar una alerta cuando una lectura superara el umbral.

**Qué implementé**

Se implementó la cadena completa:

```text
ReadingService
      ↓
AlertService
      ↓
SQLAlertRepository
      ↓
AlertModel
      ↓
alerts
```

Cuando una lectura supera el umbral configurado, `ReadingService` crea una alerta persistente asociada al sensor y a la lectura.

Además, se agregó:

```text
GET /alerts
```

para consultar las alertas almacenadas.

**Problema encontrado**

Inicialmente apareció un problema importante: las lecturas anteriores tenían:

```text
alert_triggered=True
```

pero no existían registros correspondientes en la tabla `alerts`.

Por ejemplo, la consulta de lecturas mostraba:

```text
--- READINGS CON ALERTA ---
(1, 1, 40.0, 'C', 1)
(2, 1, 40.0, 'C', 1)
(3, 2, 40.0, 'C', 1)
(4, 2, 50.0, 'C', 1)
```

mientras que la tabla de alertas solamente contenía:

```text
--- ALERTS ---
(1, 2, 4, 50.0, 35.0)
```

Por lo tanto, `GET /alerts` solamente podía devolver la alerta que realmente estaba almacenada.

**Decisión tomada**

La primera propuesta de la IA fue tratar las alertas como eventos nuevos generados durante la creación de lecturas. No acepté esa solución como explicación del comportamiento esperado de `GET /alerts`.

Mi decisión fue que el endpoint de listado debía representar **el estado completo de las alertas**, no solamente las alertas generadas desde que se conectó el nuevo servicio.

Por eso planteé una solución más sencilla: el modelo/repositorio de alertas debe consultar las alertas existentes y, cuando sea necesario reconstruirlas, utilizar las lecturas que ya tienen `alert_triggered=True`.

La razón principal fue conservar el contexto histórico. Si anteriormente existieran mil lecturas marcadas como alerta, no tendría sentido obligar al sistema a conocer solamente las alertas creadas después de la implementación del servicio.

**Verificación**

Después de corregir la integración ejecuté:

```text
pytest -q
mypy app
ruff check .
```

y obtuve:

```text
87 passed, 1 warning
```

con una cobertura total de:

```text
92.71%
```

Mypy terminó con:

```text
Success: no issues found in 31 source files
```

y Ruff:

```text
All checks passed!
```

También comprobé el endpoint `GET /alerts` desde Swagger y confirmé que las alertas almacenadas podían consultarse correctamente.

**Decisión y aprendizaje**

Esta fue la actividad donde más claramente apliqué el principio de que **la IA propone, pero yo decido**.

La IA inicialmente podía llevarme hacia una solución que funcionara para las alertas nuevas, pero cuestioné el comportamiento porque no representaba correctamente el significado de un endpoint llamado `GET /alerts`.

No acepté la primera solución solamente porque funcionara técnicamente. Revisé el modelo de datos, comprobé qué información histórica existía y elegí una solución que mantuviera el contexto de las alertas anteriores.

También confirmé que las pruebas, Mypy y Ruff son fundamentales para validar que las modificaciones propuestas por IA realmente se integren con el proyecto existente.

---

### Entrada 6 — Viernes: Validación final y retrospectiva

**Qué revisé**

Al finalizar la semana revisé que las actividades relacionadas con IA hubieran quedado integradas al proceso de desarrollo:

* prompting estructurado;
* GitHub Copilot Fundamentals;
* uso de IA local con Qwen 2.5 7B;
* trazabilidad de prompts y decisiones;
* generación asistida de pruebas;
* documentación asistida mediante ADR;
* implementación y persistencia de alertas;
* endpoint `GET /alerts`;
* validación mediante Pytest;
* validación mediante Mypy;
* validación mediante Ruff.

**Uso de IA**

Durante la semana utilicé la IA principalmente para:

* entender conceptos;
* analizar errores;
* proponer estructuras;
* generar pruebas;
* redactar documentación;
* revisar decisiones de arquitectura;
* proponer implementaciones.

Sin embargo, no acepté automáticamente sus respuestas.

El caso de las alertas fue especialmente importante porque tuve que cuestionar una propuesta de implementación. La IA estaba enfocándose en registrar las alertas generadas a partir de las nuevas lecturas, mientras que yo necesitaba que el sistema conservara y pudiera consultar el contexto histórico.

**Retrospectiva**

Esta semana confirmé que el principal riesgo de trabajar con IA no es únicamente que genere código con errores de sintaxis. Un problema más importante es que puede generar una solución **coherente pero incorrecta respecto al contexto del proyecto**.

Esto ocurrió con Qwen cuando inventó variables para las pruebas y también apareció durante la implementación de las alertas.

Por eso, mi proceso debe seguir siendo:

> **Entender el problema → pedir una propuesta → revisar la propuesta → implementarla → ejecutar las pruebas → cuestionar los resultados → corregir si es necesario.**

La IA me permitió avanzar más rápido, especialmente con documentación, pruebas y exploración de soluciones, pero las decisiones finales continuaron dependiendo de la revisión humana y de la evidencia obtenida al ejecutar el proyecto.

**Acción preventiva**

Para las siguientes semanas voy a mantener una regla más estricta:

> **No consideraré correcta una propuesta de IA hasta comprobar que coincide con el código, los datos y el comportamiento esperado del proyecto. Si la propuesta contradice el contexto existente, la cuestionaré antes de implementarla, aunque técnicamente parezca funcionar.**

Esto convierte la IA en una herramienta de apoyo al desarrollo y no en una fuente automática de decisiones arquitectónicas.



# BITÁCORA DE IA — SEMANA 6

## Consolidación de requisitos, consultas, alertas, despliegue y mantenimiento de la arquitectura

### Nota inicial

Durante el lunes y martes no se realizaron actividades de desarrollo relacionadas con SensorHub. El inicio del semestre requirió organizar las nuevas materias, horarios y actividades de servicio social, por lo que el trabajo técnico de esta semana comenzó a partir del miércoles.

La mayor parte de la semana estuvo enfocada en completar y verificar los requisitos funcionales restantes, procurando mantener la arquitectura en capas y evitar modificar innecesariamente código que ya funcionaba desde semanas anteriores.

---

### Entrada 1 — Miércoles: CRUD de sensores y validación de lecturas

**Qué necesitaba resolver**

El primer objetivo fue trabajar sobre los requisitos relacionados con la gestión de sensores.

Uno de los puntos importantes era definir correctamente el comportamiento del CRUD de sensores en producción. El requisito establece que un sensor no debe eliminarse físicamente, sino desactivarse para conservar la información histórica relacionada con él.

También se revisó el requisito de ingesta de lecturas mediante `POST`, incluyendo la validación física correspondiente al tipo de sensor.

**Prompt enviado a la IA**

> En SensorHub necesito implementar/verificar el CRUD de sensores con id, ubicación, tipo y umbral de alerta. En producción los sensores no deben eliminarse físicamente, sino desactivarse. Explícame qué significa esto y cómo debería integrarlo con la arquitectura que ya tengo sin romper las responsabilidades de las capas existentes. También revisa cómo debería manejarse la ingesta de lecturas y la validación según el tipo de sensor.

**Qué propuso la IA**

La IA explicó que la desactivación de un sensor es diferente de eliminarlo de la base de datos.

En lugar de ejecutar un `DELETE`, el sistema conserva el registro y modifica su estado para indicar que ya no está activo. De esta manera, las lecturas históricas y las relaciones con otros registros no desaparecen.

También se revisó la separación de responsabilidades:

* el router recibe la petición HTTP;
* el service contiene la lógica de negocio;
* el repository realiza el acceso a datos;
* el model representa la información persistida;
* los schemas validan los datos que pueden comprobarse únicamente con la información recibida.

**Qué implementé**

Se trabajó en el CRUD de sensores considerando el comportamiento de producción y se revisó dónde debía colocarse cada parte de la lógica para mantener la arquitectura en capas.

También se revisó el requisito de ingesta de lecturas mediante `POST`.

La validación física por tipo de sensor ya se encontraba implementada desde semanas anteriores, por lo que en esta etapa no fue necesario reconstruirla. Se corroboró que la implementación existente correspondiera con el requisito:

**RF-2 — Ingesta de lecturas con validación física por tipo de sensor.**

La validación utiliza el tipo de sensor para determinar qué unidades y rangos físicos son válidos.

**Problemas**

El principal problema durante esta parte fue entender cómo introducir nuevos comportamientos sin romper la estructura existente.

El proyecto ya tenía varias capas y servicios implementados, por lo que agregar una funcionalidad directamente en un router o modificar un repository sin considerar el resto del flujo podía terminar mezclando responsabilidades.

**Verificación**

Se revisó el comportamiento existente y se comprobó que la ingesta de lecturas ya realizaba las validaciones correspondientes.

También se verificó que la gestión de sensores siguiera el flujo de:

```text
Router → Service → Repository → Model
```

sin trasladar la lógica de negocio directamente al endpoint.

**Decisión y aprendizaje**

Esta parte reforzó una idea que ya había aparecido durante las semanas anteriores: antes de modificar código es necesario entender dónde pertenece realmente una responsabilidad.

También comprendí mejor la diferencia entre **eliminar información** y **desactivar una entidad**. Para un sistema de monitoreo, conservar los sensores históricos resulta importante porque sus lecturas anteriores siguen formando parte del historial del sistema.

---

### Entrada 2 — Jueves: consultas, paginación, alertas, estadísticas y despliegue

**Qué necesitaba resolver**

El jueves fue el día de mayor trabajo de la semana.

Primero se trabajó en el requisito de consulta de lecturas por sensor, incluyendo paginación y filtro por rango de fechas.

Después se continuó con la gestión de alertas. La detección de una lectura fuera del umbral ya estaba implementada desde semanas anteriores, por lo que el objetivo no era volver a crear esa lógica, sino construir la gestión de las alertas que ya generaba el sistema.

Finalmente se revisaron las estadísticas por sensor, el endpoint de salud y las métricas básicas.

**Prompt enviado a la IA**

> Revisa la arquitectura actual de SensorHub y ayúdame a implementar las consultas de lecturas por sensor con paginación y filtro por rango de fechas. Quiero saber en qué capa debe ir cada parte y qué archivos necesito modificar o crear. No quiero romper la separación entre router, service y repository.

**Qué propuso la IA**

La IA propuso mantener la separación de responsabilidades y hacer que los parámetros de consulta llegaran desde el router hacia el service y posteriormente al repository.

La paginación y los filtros debían formar parte de la consulta de datos, mientras que el router únicamente debía encargarse de recibir los parámetros HTTP y devolver la respuesta correspondiente.

También se revisó la estructura necesaria para que la consulta pudiera crecer posteriormente sin concentrar toda la lógica en el endpoint.

**Qué implementé**

Se agregaron y modificaron los archivos necesarios para permitir las consultas de lecturas por sensor.

Se trabajó con:

* consulta por sensor;
* paginación;
* filtro por rango de fechas;
* parámetros de consulta;
* respuesta estructurada;
* separación entre router, service y repository.

El objetivo fue que el endpoint no tuviera que conocer directamente los detalles de la consulta a la base de datos.

---

**Segunda parte: gestión de alertas**

La detección de anomalías ya existía desde semanas anteriores. Cuando una lectura supera el umbral configurado para el sensor, el sistema ya podía detectar la condición de alerta.

Por lo tanto, el trabajo de esta semana se concentró en el **RF-5 — Gestión de alertas**:

* consulta de alertas activas;
* consulta de alertas existentes;
* cambio de estado;
* estados `open`, `acknowledged` y `resolved`.

**Prompt enviado a la IA**

> Ya tengo implementada desde semanas anteriores la detección de alertas cuando una lectura supera el `alert_threshold`. Ahora necesito implementar la gestión de esas alertas: consultarlas y cambiar su estado entre `open`, `acknowledged` y `resolved`. ¿Cómo puedo agregar esto sin romper lo que ya tengo y manteniendo la separación de responsabilidades de mi arquitectura en capas?

**Qué propuso la IA**

La IA propuso mantener la detección y la gestión como responsabilidades relacionadas pero separadas.

La lógica que determina si una lectura genera una alerta debía permanecer en la lógica de negocio existente, mientras que la nueva funcionalidad debía encargarse de administrar el estado y consulta de las alertas.

La estructura debía conservar el flujo:

```text
Router
   ↓
Service
   ↓
Repository
   ↓
Model
```

**Qué implementé**

Se incorporó la gestión de las alertas existentes sin eliminar la lógica que ya funcionaba.

Esto permitió mantener la detección de anomalías separada de las operaciones posteriores sobre una alerta.

De esta forma, una alerta puede ser generada cuando corresponde y posteriormente consultarse o cambiar de estado mediante la API.

---

**Tercera parte: estadísticas y health check**

También se trabajó en los requisitos:

**RF-6 — Estadísticas por sensor y periodo**

Se implementó/verificó la obtención de estadísticas como:

* mínimo;
* máximo;
* promedio;

considerando el sensor y el periodo solicitado.

También se trabajó con:

**RF-7 — Endpoint de salud `/health` y métricas básicas.**

Se verificó que el endpoint permitiera comprobar el estado de la API y que las métricas correspondientes pudieran obtenerse sin mezclar esta responsabilidad con la lógica principal de sensores y lecturas.

**Problemas**

Uno de los problemas más importantes apareció al intentar llevar los cambios a producción.

En local, los cambios funcionaban correctamente, pero al desplegarlos en Render apareció un error relacionado con **Alembic y las migraciones de la base de datos**.

Inicialmente pensé que el problema estaba en mi código y pasé varias horas revisando las modificaciones realizadas.

Después de revisar con mayor detalle el comportamiento de Render, descubrí que el problema estaba relacionado con una migración anterior que había quedado registrada en la base de datos de producción.

Esa migración había quedado vacía, posteriormente fue eliminada y se creó otra migración correcta, pero Render conservaba el historial anterior en su base de datos. Por lo tanto, Alembic intentaba ejecutar una migración cuyo identificador ya no coincidía con los archivos existentes en el repositorio.

**Qué cambié**

En lugar de continuar modificando código de la aplicación intentando solucionar un problema que ya no correspondía a la implementación, investigué el estado del despliegue y de las migraciones almacenadas en Render.

Consulté a la IA sobre cómo reiniciar el entorno de Render y posteriormente realicé nuevamente el despliegue manual.

**Verificación**

Después de reiniciar el entorno y ejecutar el **Manual Deploy**, Render pudo ejecutar correctamente las migraciones y levantar nuevamente el servidor con los cambios actuales.

Esto permitió comprobar que el problema no estaba en la lógica nueva de SensorHub, sino en el estado anterior de la base de datos de producción y su historial de migraciones.

**Decisión y aprendizaje**

Esta experiencia fue importante porque inicialmente estaba buscando el error únicamente dentro de mi código.

Aprendí que cuando una aplicación funciona correctamente en local pero falla durante el despliegue, también hay que revisar el estado del entorno de producción, las migraciones almacenadas y la configuración del servicio.

La IA fue útil para orientar la investigación, pero la solución no consistió simplemente en copiar una modificación de código. Primero tuve que identificar que el problema estaba fuera de la aplicación.

---

### Entrada 3 — Viernes: Pull Request, logs estructurados y validación final

**Qué necesitaba resolver**

El viernes se concentró principalmente en preparar los cambios realizados durante la semana y llevarlos al flujo de revisión mediante Pull Request.

También se revisó la arquitectura general del proyecto y se identificó un punto que todavía podía mejorarse: los logs.

La arquitectura en capas ya estaba funcionando correctamente en términos generales, por lo que no era necesario realizar una reorganización importante.

El cambio principal de esta parte fue implementar **logs estructurados**.

**Prompt enviado a la IA**

> Mi arquitectura en capas ya está funcionando y no quiero hacer cambios innecesarios en routers, services, repositories, models y schemas. Necesito mejorar únicamente los logs para que sean estructurados y útiles para diagnosticar errores y revisar el comportamiento de la API. Explícame qué debería cambiar y en qué parte de la arquitectura debería hacerlo.

**Qué propuso la IA**

La IA propuso centralizar el formato de los registros y utilizar información estructurada en lugar de depender únicamente de mensajes de texto diferentes en cada parte del proyecto.

Esto permite que los logs sean más fáciles de interpretar y posteriormente procesar.

También recomendó evitar introducir lógica de logging específica dentro de cada capa cuando pudiera resolverse mediante una configuración común.

**Qué implementé**

Se modificó la configuración de logs para utilizar un formato más estructurado.

El objetivo fue mantener información útil para identificar qué ocurrió durante la ejecución de la API sin modificar innecesariamente las responsabilidades de las capas.

La arquitectura principal continuó manteniendo la separación existente entre:

```text
Routers
   ↓
Services
   ↓
Repositories
   ↓
Models
```

mientras que los schemas continuaron funcionando como contratos de entrada y salida.

**Verificación**

Se revisó que los cambios de la semana no rompieran la arquitectura existente y se ejecutaron las validaciones disponibles del proyecto.

También se comprobó nuevamente el funcionamiento de la API y el despliegue en producción después de solucionar el problema de las migraciones de Render.

Finalmente, los cambios quedaron preparados para el Pull Request correspondiente.

**Decisión y aprendizaje**

El aprendizaje principal del viernes fue que no todas las semanas requieren una modificación arquitectónica grande.

En este caso, la arquitectura en capas ya estaba cumpliendo correctamente su función. La prioridad fue agregar funcionalidades nuevas sin romper las responsabilidades que ya estaban definidas.

También confirmé que los logs forman parte importante de la operación de una API en producción. Una aplicación puede funcionar correctamente, pero si no deja información suficiente para diagnosticar errores, resulta mucho más difícil mantenerla.

---

## Retrospectiva de la semana

Durante esta semana el trabajo estuvo principalmente enfocado en completar los requisitos funcionales restantes de SensorHub y llevarlos a un estado más cercano a producción.

Se trabajó principalmente en:

* **RF-1:** CRUD de sensores y comportamiento de desactivación en producción.
* **RF-2:** verificación de la ingesta de lecturas y validación física por tipo de sensor.
* **RF-3:** consultas de lecturas por sensor, paginación y filtros por rango de fechas.
* **RF-4:** verificación de la detección de anomalías y generación de alertas.
* **RF-5:** consulta y gestión del estado de las alertas.
* **RF-6:** estadísticas por sensor y periodo.
* **RF-7:** endpoint `/health` y métricas básicas.
* **RNF-5:** mejora de los logs estructurados.
* Preparación de los cambios para revisión mediante Pull Request.

La mayor dificultad de la semana no estuvo directamente en escribir código, sino en **integrar nuevas funcionalidades con una arquitectura que ya tenía varias piezas funcionando**.

Por eso, gran parte de las consultas realizadas a la IA estuvieron orientadas a preguntas como:

* ¿En qué capa debería colocar esta lógica?
* ¿Qué archivo debería modificar?
* ¿Cómo puedo obtener este dato sin acoplar las clases?
* ¿Cómo puedo agregar esta funcionalidad sin romper lo que ya existe?
* ¿Cómo puedo mantener la separación de responsabilidades?
* ¿Cómo puedo reutilizar la lógica que ya existe?

El problema de Render también mostró que un error durante el despliegue no necesariamente significa que el código de la aplicación esté incorrecto. En este caso, la causa estaba relacionada con el historial de migraciones almacenado en el entorno de producción.

La experiencia de esta semana reforzó el proceso que ya había establecido anteriormente:

> **Entender → preguntar → analizar la propuesta → implementar → ejecutar → verificar → corregir.**

La IA funcionó principalmente como una herramienta para localizar dónde hacer los cambios y entender las relaciones entre las diferentes partes del proyecto. La decisión final sobre qué implementar se tomó comparando sus propuestas con el código real, los requisitos y el comportamiento esperado de SensorHub.

## Aprendizaje final

Esta semana comprendí mejor que mantener una arquitectura no significa evitar modificar el código, sino **modificarlo respetando las responsabilidades que ya existen**.

También confirmé que una solución técnicamente válida no necesariamente es la solución correcta para el proyecto. Esto ocurrió especialmente durante la depuración del despliegue en Render: durante varias horas asumí que el problema estaba en mi implementación cuando realmente estaba relacionado con el estado de las migraciones en producción.

Por ello, continúo utilizando la IA como apoyo para comprender, investigar y proponer soluciones, pero la validación final depende del comportamiento real del proyecto y de las pruebas realizadas.
