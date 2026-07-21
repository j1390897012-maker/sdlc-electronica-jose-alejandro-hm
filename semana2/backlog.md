# Product Backlog – Sistema Inteligente de Monitoreo Ambiental

## Descripción del producto

Sistema encargado de monitorear variables ambientales mediante sensores,
permitiendo registrar, visualizar, almacenar y analizar mediciones obtenidas
en un entorno supervisado.

---

# User Stories

## US-01: Consultar historial de mediciones

**Story Points:** 3

**Como** operador de planta,

**quiero** consultar el historial de mediciones de un sensor específico,

**para** analizar su comportamiento a lo largo del tiempo.

## Criterios de aceptación:

**Escenario:** Consultar el historial de un sensor registrado

**Given** un sensor con id "TEMP-01" registrado en el sistema,

**When** el operador consulta el historial del sensor "TEMP-01",

**Then** el sistema muestra todas las mediciones registradas del sensor,

**And** las mediciones aparecen ordenadas por fecha y hora

---

**Escenario:** Consultar un sensor inexistente

**Given** que no existe ningún sensor con id "TEMP-99"

**When** el operador consulta el historial del sensor "TEMP-99"

**Then** el sistema informa que el sensor no fue encontrado

**And** no muestra ninguna medición

## US-02: Registrar un nuevo sensor

**Story Points:** 3

**Como** operador de planta,

**quiero** registrar un nuevo sensor,

**para** comenzar a monitorear sus mediciones dentro del sistema.

---

## Criterios de aceptacion:

**Escenario:** Registrar un nuevo sensor correctamente

**Given** el sistema está disponible para registrar sensores

**When** el operador agrega un sensor con nombre "HUM01"

**Then** el sistema muestra el mensaje "Nuevo sensor agregado"

**And** el operador puede visualizar el sensor "HUM01" en la lista de sensores

---

**Escenario:** Registrar un sensor con nombre repetido

**Given** existe un sensor registrado con nombre "HUM01"

**When** el operador intenta agregar otro sensor llamado "HUM01"

**Then** el sistema muestra un mensaje de error indicando que el sensor ya existe

---

## US-03: Eliminar un sensor

**Story Points:** 2

**Como** operador de planta,

**quiero** eliminar un sensor existente,

**para** dejar de monitorear sensores que ya no sean necesarios.

---

## Criterios de aceptacion:

**Escenario:** Eliminar un sensor correctamente

**Given** existe un sensor registrado con nombre "HUM01"

**When** el operador elimina el sensor "HUM01"

**Then** el sistema muestra el mensaje "Sensor eliminado"

**And** el sensor "HUM01" ya no aparece en la lista de sensores

---

**Escenario:** Eliminar un sensor inexistente

**Given** no existe un sensor con nombre "HUM99"

**When** el operador intenta eliminar el sensor "HUM99"

**Then** el sistema muestra un mensaje indicando que el sensor no existe

---

## US-04: Visualizar temperatura en tiempo real

**Story Points:** 5

**Como** operador de planta,

**quiero** visualizar la temperatura en tiempo real,

**para** tomar decisiones rápidas sobre el funcionamiento de la planta.

---

## Criterios de aceptacion:

**Escenario:** Visualizar temperatura de un sensor en tiempo real

**Given** existe un sensor de temperatura registrado con nombre "TEMP01"

**When** el operador selecciona el sensor "TEMP01"

**Then** el sistema muestra la lectura actual de temperatura en tiempo real

**And** la lectura se actualiza conforme llegan nuevas mediciones

---

**Escenario:** Visualizar temperatura de un sensor sin conexión

**Given** existe un sensor de temperatura registrado pero sin conexión

**When** el operador selecciona el sensor "TEMP01"

**Then** el sistema muestra un mensaje indicando que el sensor no está disponible

---

## US-05: Exportar mediciones

**Story Points:** 5

**Como** operador de planta,

**quiero** exportar las mediciones a un archivo CSV,

**para** analizarlas posteriormente utilizando otras herramientas.

---

## Criterios de aceptacion:

**Escenario:** Exportar mediciones correctamente

**Given** existe un sensor con mediciones almacenadas en el sistema

**When** el operador solicita exportar las mediciones a formato CSV

**Then** el sistema genera un archivo CSV con los datos del sensor

**And** el archivo contiene fecha, hora y valor de cada medición

---

**Escenario:** Exportar mediciones sin datos disponibles

**Given** existe un sensor registrado sin mediciones almacenadas

**When** el operador intenta exportar sus mediciones

**Then** el sistema informa que no existen datos disponibles para exportar

---

## US-06: Visualizar historial mediante gráficas

**Story Points:** 8

**Como** operador de planta,

**quiero** visualizar el historial de mediciones mediante gráficas,

**para** identificar tendencias y cambios en el comportamiento de los sensores.

---

## Criterios de aceptacion:

**Escenario:** Mostrar gráfica de mediciones históricas

**Given** existe un sensor con mediciones almacenadas

**When** el operador consulta la gráfica del sensor

**Then** el sistema muestra una gráfica con los valores registrados

**And** la gráfica permite identificar cambios en las mediciones a través del tiempo

---

**Escenario:** Mostrar gráfica sin mediciones

**Given** existe un sensor sin historial de mediciones

**When** el operador solicita visualizar la gráfica

**Then** el sistema informa que no existen datos suficientes para generar la gráfica

---

## US-07: Recibir alertas por valores críticos

**Story Points:** 8

**Como** operador de planta,

**quiero** recibir alertas cuando los valores de los sensores superen los umbrales configurados,

**para** tomar medidas preventivas o correctivas de manera inmediata.

---

## Criterios de aceptacion:

**Escenario:** Generar alerta por valor fuera del límite permitido

**Given** existe un sensor con un umbral configurado

**When** el sensor registra un valor superior al límite establecido

**Then** el sistema genera una alerta para el operador

**And** muestra el sensor y valor que generó la alerta

---

**Escenario:** No generar alerta cuando el valor está dentro del rango

**Given** existe un sensor con un umbral configurado

**When** el sensor registra un valor dentro del rango permitido

**Then** el sistema no genera ninguna alerta

---

## US-08: Configurar umbrales de sensores

**Story Points:** 5

**Como** operador de planta,

**quiero** configurar los umbrales de los sensores,

**para** personalizar las condiciones que generan alertas según las necesidades de la planta.

---

## Criterios de aceptacion:

**Escenario:** Configurar un nuevo umbral correctamente

**Given** existe un sensor registrado en el sistema

**When** el operador configura un nuevo valor límite para el sensor

**Then** el sistema guarda la nueva configuración del umbral

**And** utiliza ese valor para generar futuras alertas

---

**Escenario:** Configurar un umbral con valor inválido

**Given** existe un sensor registrado en el sistema

**When** el operador introduce un valor de umbral inválido

**Then** el sistema muestra un mensaje indicando que el valor no es válido

---

## US-09: Buscar un sensor

**Story Points:** 2

**Como** operador de planta,

**quiero** buscar un sensor específico,

**para** acceder rápidamente a su información y mediciones.

---

## Criterios de aceptacion:

**Escenario:** Buscar un sensor registrado

**Given** existe un sensor registrado con nombre "TEMP01"

**When** el operador busca el sensor "TEMP01"

**Then** el sistema muestra la información del sensor encontrado

---

**Escenario:** Buscar un sensor inexistente

**Given** no existe un sensor llamado "TEMP99"

**When** el operador busca el sensor "TEMP99"

**Then** el sistema informa que no encontró resultados

---

## US-10: Consultar estado de sensores

**Story Points:** 3

**Como** operador de planta,

**quiero** consultar el estado de los sensores (activo/inactivo),

**para** verificar su correcto funcionamiento dentro del sistema.

---

## Criterios de aceptacion:

**Escenario:** Consultar estado de un sensor activo

**Given** existe un sensor conectado al sistema

**When** el operador consulta el estado del sensor

**Then** el sistema muestra el estado "Activo"

---

**Escenario:** Consultar estado de un sensor desconectado

**Given** existe un sensor registrado pero sin conexión

**When** el operador consulta el estado del sensor

**Then** el sistema muestra el estado "Inactivo"

---

## US-11: Visualizar sensores seleccionados en la pantalla principal

**Story Points:** 3

**Como** operador de planta,

**quiero** visualizar sensores seleccionados en la pantalla principal,

**para** monitorearlos rápidamente sin necesidad de buscarlos constantemente.

---

## Criterios de aceptacion:

**Escenario:** Mostrar sensores seleccionados en pantalla principal

**Given** existen sensores registrados en el sistema

**When** el operador selecciona sensores favoritos

**Then** el sistema muestra esos sensores en la pantalla principal

**And** permite consultar sus valores sin realizar una búsqueda

---

**Escenario:** No mostrar sensores eliminados

**Given** un sensor seleccionado fue eliminado del sistema

**When** el operador accede a la pantalla principal

**Then** el sistema deja de mostrar ese sensor