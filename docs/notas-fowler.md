# Notas de lectura — Martin Fowler

## Microservices

### Idea principal

Los microservicios son una forma de construir una aplicación como un conjunto de servicios pequeños que:

- se ejecutan como procesos independientes;
- se comunican mediante mecanismos ligeros, normalmente APIs;
- están organizados alrededor de capacidades de negocio;
- pueden desplegarse de manera independiente.

Por lo tanto, microservicios no significa simplemente "hacer muchas clases pequeñas" ni "separar el código en carpetas".

### Características importantes

- Los servicios tienen límites claros.
- Cada servicio representa una capacidad de negocio.
- Los servicios pueden desplegarse de manera independiente.
- Cada servicio puede utilizar tecnologías diferentes.
- La gestión y los datos están más descentralizados.
- Se necesita automatización de infraestructura y despliegue.
- El sistema debe diseñarse considerando que los servicios pueden fallar.

### Ventajas

- Límites de módulos más fuertes.
- Posibilidad de desplegar servicios de manera independiente.
- Posibilidad de escalar solamente los componentes que lo necesiten.
- Mayor libertad tecnológica entre servicios.
- Equipos diferentes pueden trabajar de forma más autónoma.

### Costos

Los microservicios también agregan complejidad:

- Las llamadas entre procesos son más lentas que las llamadas dentro del mismo proceso.
- Las comunicaciones de red pueden fallar.
- La consistencia de datos se vuelve más complicada.
- Hay más infraestructura que administrar.
- Las pruebas y el monitoreo se vuelven más complejos.

Por eso Fowler señala que muchas situaciones funcionan mejor con un monolito.

### Relación con mi proyecto

Mi proyecto actualmente NO utiliza microservicios.

La aplicación es una sola API FastAPI y las capas
routers -> services -> repositories -> models
están dentro del mismo proceso.

Esto es una arquitectura en capas dentro de un monolito, no una arquitectura distribuida.

La separación de responsabilidades que tengo actualmente puede ayudar
a mantener buenos límites internos si en el futuro el proyecto creciera,
pero eso no significa que actualmente deba dividirse en microservicios.


## Monolith First

### Idea principal

Fowler propone considerar una estrategia de "Monolith First":

Construir primero un monolito bien estructurado y solamente dividirlo
en microservicios cuando exista suficiente conocimiento sobre el sistema
y realmente exista una razón para hacerlo.

### ¿Por qué?

Al comenzar un proyecto todavía existe incertidumbre:

- No sabemos con certeza qué funcionalidades serán importantes.
- No conocemos todavía los límites correctos entre componentes.
- El producto puede incluso no resultar útil para los usuarios.
- Cambiar los límites dentro de un monolito es más sencillo que cambiar
  los límites entre servicios distribuidos.

Por eso comenzar directamente con microservicios puede hacer que las
decisiones arquitectónicas equivocadas sean mucho más costosas de cambiar.

### Límites de los servicios

Uno de los puntos que más me llamó la atención es que definir correctamente
los límites de los microservicios es difícil.

Si una funcionalidad se coloca en el servicio equivocado, posteriormente
moverla puede requerir comunicación entre servicios, cambios de APIs,
manejo de datos distribuidos y más coordinación.

Dentro de un monolito modular es mucho más sencillo reorganizar estas
responsabilidades.

### Microservice Premium

Los microservicios tienen un costo adicional de operación y desarrollo.

Ese costo puede estar justificado en sistemas grandes y complejos,
pero no necesariamente en un proyecto pequeño.

Por eso no tendría sentido introducir microservicios solamente porque
son una arquitectura moderna o popular.

### Aplicación a mi proyecto

Para mi proyecto tiene más sentido mantener inicialmente un monolito
bien organizado.

La arquitectura en capas me permite practicar separación de
responsabilidades y DIP sin introducir todavía la complejidad de una
arquitectura distribuida.

Si el proyecto creciera, primero tendría que identificar límites de
negocio reales y comprobar que existe una necesidad de separar servicios.

No debería convertir automáticamente cada capa actual en un microservicio.


## Conclusiones para discusión

### 1. ¿Arquitectura en capas significa microservicios?

No.

Las capas organizan responsabilidades dentro de una aplicación.

Los microservicios separan la aplicación en servicios independientes
que normalmente se ejecutan en procesos diferentes y se comunican
mediante mecanismos de red.

### 2. ¿Por qué no usar microservicios desde el principio?

Porque todavía no conocemos suficientemente bien el dominio ni los
límites correctos del sistema.

Además, los microservicios introducen costos operativos y de comunicación
que pueden ser innecesarios para un proyecto pequeño.

### 3. ¿Qué aprendí de Fowler?

La arquitectura no debe elegirse solamente porque una tecnología sea
popular.

Debe evaluarse según el contexto, los problemas que intenta resolver
y los costos que introduce.

### 4. Relación con mi ADR

Mi ADR de arquitectura en capas busca precisamente mantener separadas
las responsabilidades dentro del monolito:

routers -> services -> repositories -> models

Además, los services dependen de Protocols para los repositorios,
lo que permite utilizar FakeRepositories durante las pruebas.

Esto proporciona modularidad sin introducir todavía la complejidad
operativa de los microservicios.

### 5. Decisión personal

Para el proyecto actual mantendría la arquitectura como un monolito
bien estructurado.

No introduciría microservicios por ahora.

Si el sistema creciera y aparecieran necesidades reales de despliegue
independiente, escalamiento independiente o límites de negocio claramente
separados, entonces evaluaría una migración progresiva.
