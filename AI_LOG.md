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
