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

