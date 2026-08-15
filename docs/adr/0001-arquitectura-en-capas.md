# ADR 0001: Arquitectura en capas

## Estado

Aceptado.

## Contexto

SensorHub API es una API construida con FastAPI para la gestión de sensores
(`SensorModel`) y de las lecturas que estos producen (`ReadingModel`). El
código en `app/` está organizado en cinco paquetes con responsabilidades
diferenciadas: `routers`, `services`, `repositories`, `models` y `schemas`.

Esta separación responde a varios problemas concretos que aparecen en el
dominio del proyecto:

- **Reglas de negocio no triviales que no pueden vivir en la validación de
  entrada.** Por ejemplo, `ReadingService._validate_reading` necesita
  consultar el sensor asociado a una lectura para conocer su tipo
  (`temperature`, `humidity`, `pressure`) antes de poder validar la unidad y
  el rango físico del valor recibido. El propio docstring del método explica
  que "esta validación vive aquí y no en Pydantic porque necesita consultar
  el sensor en la base de datos para saber su tipo". Esa dependencia de un
  dato persistido descarta que la validación pueda resolverse únicamente en
  los `schemas` de entrada.
- **Necesidad de aislar el acceso a datos.** Tanto sensores como lecturas se
  persisten mediante SQLAlchemy (`SQLSensorRepository`, `SQLReadingRepository`
  operando sobre una `Session`), pero la lógica de negocio (`SensorService`,
  `ReadingService`) no debía quedar acoplada a SQLAlchemy para poder probarse
  sin una base de datos real.
- **Necesidad de que los endpoints HTTP no concentren lógica de negocio.**
  Los docstrings de `app/routers/sensors.py` y `app/routers/readings.py` son
  explícitos al respecto: "Solo traduce entre HTTP y SensorService: no
  contiene lógica de negocio" y "Solo traduce entre HTTP y ReadingService: no
  contiene lógica de negocio", respectivamente. Cada router se limita a
  invocar el servicio correspondiente y traducir sus resultados o
  excepciones de dominio a códigos de estado HTTP.
- **Necesidad de notificar alertas sin acoplar el dominio a un mecanismo de
  notificación concreto.** Cuando una lectura supera el `alert_threshold`
  configurado en un sensor, `ReadingService._check_alert` debe disparar una
  notificación (US-07), pero sin que la lógica de negocio dependa de que esa
  notificación se imprima en consola, se envíe por correo o cualquier otro
  canal.

## Decisión

Se adopta una **arquitectura en capas** para `app/`, con las siguientes
responsabilidades verificadas en el código:

### Routers (`app/routers/sensors.py`, `app/routers/readings.py`)

Definen los endpoints REST con `APIRouter` de FastAPI. Reciben la petición
HTTP, la delegan al servicio correspondiente obtenido vía `Depends`
(`get_sensor_service`, `get_reading_service`), y traducen el resultado o las
excepciones de dominio a respuestas HTTP: por ejemplo, `sensors.py` mapea
`SensorDuplicadoError` a 409 y `ValueError` a 400; `readings.py` mapea
`LookupError` a 404 y `ValueError` a 400. No contienen reglas de negocio,
según indican explícitamente sus propios docstrings.

### Services (`app/services/sensor_service.py`, `app/services/reading_service.py`)

Contienen la lógica de negocio del proyecto: `SensorService.create` valida
que no exista ya un sensor con el mismo nombre (lanzando
`SensorDuplicadoError`); `SensorService.update` revalida la combinación
tipo/unidad antes de persistir cambios; `ReadingService._validate_reading`
valida existencia del sensor, unidad compatible con su tipo y rangos físicos
según el tipo de sensor; `ReadingService._check_alert` evalúa el umbral de
alerta (US-08) y notifica cuando se supera (US-07). Los servicios reciben
sus dependencias (repositorios, notificador) por constructor y no las
instancian ellos mismos.

### Repositories (`app/repositories/`)

Encapsulan el acceso a datos. Existen dos implementaciones por recurso:

- `SQLSensorRepository` y `SQLReadingRepository`, que operan sobre una
  `Session` de SQLAlchemy y son las que se inyectan en producción (ver
  `get_sensor_service` y `get_reading_service` en los routers).
- `FakeSensorRepository` y `FakeReadingRepository`, que guardan los datos en
  listas en memoria y se usan exclusivamente en pruebas.

### Models (`app/models/sensor.py`, `app/models/reading.py`)

Son los modelos ORM de SQLAlchemy (`SensorModel`, `ReadingModel`), mapeados
a las tablas `sensors` y `readings`. `ReadingModel.sensor_id` es una FK real
hacia `sensors.id`, y la relación `SensorModel.readings` usa
`cascade="all, delete-orphan"`. Representan la estructura persistida, no el
contrato de entrada/salida de la API.

### Schemas (`app/schemas/sensor.py`, `app/schemas/reading.py`)

Son modelos Pydantic (`SensorCreate`, `SensorUpdate`, `SensorOut`,
`SensorReadingIn`, `SensorReadingOut`, `SensorReadingUpdate`) que definen el
contrato de entrada y salida de la API. Ejecutan validaciones que sí pueden
resolverse solo con los datos de la propia petición, como
`SensorCreate.validate_unit`, que rechaza combinaciones tipo/unidad
inválidas usando `VALID_UNITS`. Las validaciones que requieren datos ya
persistidos (por ejemplo, el tipo de un sensor existente al registrar una
lectura) se hacen en los services, no en los schemas.

### Abstracciones mediante `Protocol`

El proyecto usa `typing.Protocol` en **dos** puntos concretos, no en todas
las capas:

- `SensorRepository` (`app/repositories/sensor_repository.py`) y
  `ReadingRepository` (`app/repositories/reading_repository.py`) son
  `Protocol` que definen el contrato de persistencia. `SensorService` y
  `ReadingService` reciben una instancia que cumple estos protocolos por
  constructor (tipada como `SensorRepository` / `ReadingRepository`), sin
  importar `SQLSensorRepository` ni `SQLReadingRepository` en su módulo.
- `AlertNotifier` (`app/services/alert_notifier.py`) es también un
  `Protocol`, con dos implementaciones: `ConsoleAlertNotifier` (por defecto
  en producción) y `FakeAlertNotifier` (para pruebas). `ReadingService`
  recibe un `AlertNotifier | None` por constructor y usa
  `ConsoleAlertNotifier()` como valor por defecto si no se provee ninguno.

Los `schemas` (Pydantic) y los `models` (SQLAlchemy ORM) **no** usan
`Protocol`: son clases concretas de sus respectivos frameworks. No se debe
asumir que todas las capas del proyecto se abstraen mediante `Protocol`;
solo los repositorios y el notificador de alertas lo hacen.

## Consecuencias

### Positivas

- **Los servicios se prueban sin base de datos real.** `tests/test_sensor_service.py`
  y `tests/test_reading_service.py` instancian `SensorService` y
  `ReadingService` con `FakeSensorRepository` y `FakeReadingRepository` en
  lugar de las implementaciones SQL, lo que hace las pruebas rápidas y sin
  dependencias externas.
- **`ReadingService` puede probarse sin depender de consola real**, gracias
  a `FakeAlertNotifier`, que registra los mensajes de alerta en una lista en
  memoria en lugar de imprimirlos.
- **Los routers quedan simples y enfocados en la traducción HTTP.** No
  necesitan conocer reglas de negocio ni detalles de persistencia; solo
  invocan el servicio inyectado y mapean sus resultados/excepciones a
  respuestas HTTP.
- **Las reglas de negocio quedan centralizadas.** Validaciones como los
  rangos físicos por tipo de sensor o la evaluación del umbral de alerta
  viven en un único lugar (los services), evitando duplicarlas entre
  routers y repositorios.
- **Es posible cambiar el mecanismo de persistencia o de notificación sin
  tocar la lógica de negocio**, siempre que la nueva implementación cumpla
  el `Protocol` correspondiente (`SensorRepository`, `ReadingRepository` o
  `AlertNotifier`).

### Negativas

- **Más archivos e indirección para cada operación.** Una misma operación
  (por ejemplo, crear un sensor) atraviesa router → service → repository →
  model, lo que implica más saltos entre archivos que una solución con toda
  la lógica en el router o en el modelo.
- **Riesgo de duplicar validaciones entre `schemas` y `services`** si no se
  es disciplinado sobre qué validación va en cada capa. Por ejemplo, la
  validación de unidad según tipo aparece tanto en `SensorCreate.validate_unit`
  (schema) como en `SensorService.update` (service), aunque para casos
  distintos: creación (donde todos los datos llegan en la petición) frente a
  actualización parcial (donde el service necesita combinar el patch con el
  estado ya persistido).
- **Los repositorios `Fake*` deben mantenerse manualmente en sincronía con
  el `Protocol` y con el comportamiento de la implementación SQL** para que
  las pruebas sigan siendo representativas; no hay un mecanismo automático
  en el proyecto que garantice esa equivalencia.
- **Curva de entrada algo mayor** para quien no conozca el patrón: entender
  el flujo completo de una feature requiere leer router, service,
  repository, model y schema, en vez de un único archivo.

### Relación con el principio DIP (Dependency Inversion Principle)

`SensorService` y `ReadingService` dependen de las abstracciones
`SensorRepository` y `ReadingRepository` (`Protocol`), no de
`SQLSensorRepository` ni `SQLReadingRepository` directamente: ambas clases
concretas se importan únicamente en los routers, donde se construyen e
inyectan (`get_sensor_service`, `get_reading_service`). Esto es explícito en
los propios docstrings de `sensor_service.py` y `reading_service.py`, que
mencionan el DIP y remiten a `tests/test_sensor_service.py` como evidencia
de que el servicio puede sustituir la implementación real por
`FakeSensorRepository` sin modificar su código. Lo mismo aplica a
`AlertNotifier`: `ReadingService` depende del `Protocol`, no de
`ConsoleAlertNotifier`, lo que permite sustituirlo por `FakeAlertNotifier`
en pruebas.

### Por qué esto no implica una arquitectura de microservicios

Adoptar una arquitectura en capas es una decisión sobre cómo se organiza el
código **dentro de un mismo proceso y un mismo despliegue**, no sobre cómo
se distribuye el sistema en la red. En este proyecto:

- Existe una única aplicación FastAPI (`app = FastAPI(...)` en
  `app/main.py`), que registra los routers de `sensors` y `readings` en el
  mismo proceso (`app.include_router(sensors.router)`,
  `app.include_router(readings.router)`).
- Routers, services, repositories, models y schemas se ejecutan en el mismo
  proceso Python, se comunican mediante llamadas a función directas (no HTTP,
  colas de mensajes ni RPC) y comparten la misma base de datos a través del
  mismo `engine`/`Session` definidos en `app/db.py`.
- No hay evidencia en el código de múltiples servicios desplegables por
  separado, cada uno con su propia base de datos o API pública independiente,
  que es lo que caracteriza a una arquitectura de microservicios.

En otras palabras: las capas dividen **responsabilidades dentro de la
aplicación** (presentación, negocio, acceso a datos), mientras que los
microservicios dividirían **la aplicación misma** en unidades desplegables
independientes. Ambas son decisiones ortogonales, y este proyecto solo
adopta la primera.