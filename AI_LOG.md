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
