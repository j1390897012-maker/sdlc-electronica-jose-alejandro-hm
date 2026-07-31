# Bitácora de IA – Semana 3

## Desarrollo de la API y organización del proyecto

---

# Entrada 1 – Comprensión de los temas y preparación del trabajo

## Uso de IA:

Durante esta etapa utilicé la IA principalmente para entender los temas que se iban a trabajar durante cada día y para tener una idea más clara de qué debía hacer antes de comenzar a programar.

Como varios de los conceptos eran nuevos para mí, primero preguntaba qué significaba cada cosa, para qué servía y cómo se relacionaba con el proyecto que ya estaba desarrollando.

También utilicé la IA para buscar palabras clave que pudiera utilizar en YouTube y complementar la información con videos y explicaciones de otras fuentes.

## Preguntas realizadas:

Durante los primeros días pregunté sobre los temas que se tenían que desarrollar. Por ejemplo, cuando tocó trabajar con la API, pregunté qué era una API, cómo funcionaba, cómo se podía lanzar una API en Python y cómo se conectaba con las partes del proyecto que ya tenía.

También pregunté sobre los diferentes componentes que se iban a utilizar, qué función tenía cada uno y cómo se relacionaban entre sí.

Además, cuando algún concepto no me quedaba completamente claro, pedía explicaciones más sencillas y ejemplos relacionados con mi propio proyecto en lugar de quedarme solamente con una definición.

## Sugerencia recibida:

La IA me ayudó primero a dividir los temas en conceptos más pequeños y después relacionarlos con el proyecto.

También me proporcionó palabras clave y temas específicos que podía buscar en YouTube para complementar lo aprendido. Esto me permitió no depender solamente de una explicación de IA y buscar otras formas de entender los conceptos.

## Decisión tomada:

Decidí utilizar la IA principalmente como una herramienta para entender qué iba a hacer antes de comenzar a programarlo.

Cuando un concepto no lo entendía, primero intentaba comprenderlo y después buscaba información adicional mediante videos y otros recursos.

## Cambios realizados:

Antes de implementar las funcionalidades fui organizando mentalmente qué partes necesitaba modificar y qué relación tenían con el código que ya existía.

Esto me permitió comenzar la implementación con una idea más clara de lo que debía construir.

## Resultado:

La IA me permitió tener una visión inicial de los temas de cada día, entender conceptos que todavía no dominaba y encontrar mejores términos para buscar información adicional.

Esto hizo que pudiera comenzar el desarrollo con una idea más clara y no simplemente programar sin saber qué estaba haciendo.

---

# Entrada 2 – Organización y planificación de los cambios

## Uso de IA:

Después de entender los temas que se tenían que trabajar, utilicé la IA para organizar la forma en que iba a realizar los cambios dentro del proyecto.

Yo normalmente tenía una idea de cómo quería hacer las cosas y se la explicaba a la IA. A partir de esa idea, revisábamos si la estructura tenía sentido y qué cosas podían agregarse o cambiarse.

## Preguntas realizadas:

Le explicaba a la IA lo que quería conseguir y preguntaba cómo sería mejor organizarlo dentro del proyecto.

También preguntaba dónde debía colocar determinada funcionalidad, qué archivos tenían que modificarse y si la forma en que estaba pensando hacerlo podía generar problemas posteriormente.

En varias ocasiones yo proponía una estructura y la IA me indicaba que podía funcionar, pero que sería mejor agregar o modificar algunas cosas para mantener una mejor organización.

## Sugerencia recibida:

La IA me ayudó a dividir las funcionalidades entre diferentes archivos y responsabilidades en lugar de intentar colocar todo en un mismo lugar.

También me explicó el motivo de realizar determinadas separaciones y cómo los cambios en una parte del proyecto podían afectar a otras partes.

## Decisión tomada:

Acepté algunas de las sugerencias y otras las fui modificando de acuerdo con lo que necesitaba el proyecto.

La intención no era simplemente copiar lo que decía la IA, sino utilizar sus propuestas para comparar diferentes formas de realizar una misma funcionalidad y decidir cuál tenía más sentido.

## Cambios realizados:

Se reorganizaron diferentes partes de la aplicación relacionadas con modelos, esquemas, servicios, repositorios, routers y pruebas.

También se fueron actualizando las pruebas conforme cambiaba la estructura del sistema.

## Resultado:

La organización permitió trabajar de una manera más ordenada y entender mejor qué responsabilidad tenía cada parte del proyecto.

También ayudó a evitar que todo el código terminara dependiendo directamente de una sola clase o archivo.

---

# Entrada 3 – Corrección, integración y depuración del proyecto

## Uso de IA:

Esta fue la etapa en la que más utilicé la IA durante el desarrollo.

Durante aproximadamente desde las 10 de la mañana hasta las 5 de la tarde estuve trabajando principalmente en corregir, conectar y depurar los cambios realizados en el proyecto.

El problema principal fue que ya existían varios archivos y carpetas relacionados entre sí. Al modificar una parte, muchas veces era necesario modificar otra parte para que las referencias, llamadas y tipos coincidieran.

## Problemas encontrados:

Al cambiar una función o una clase, aparecían errores en otros archivos que dependían de ella.

Por ejemplo, al modificar la forma en que se manejaban las lecturas, también era necesario revisar los servicios, repositorios, routers y pruebas que utilizaban esas funciones.

Esto provocó varios errores durante el proceso, porque una modificación que parecía pequeña podía afectar diferentes partes del proyecto.

También tuve que revisar constantemente qué archivo llamaba a qué función, qué parámetros esperaba cada método y qué tipo de dato estaba recibiendo.

En algunos momentos utilicé otra inteligencia artificial para ayudarme a separar y analizar partes específicas del código y poder identificar mejor dónde estaba el problema.

## Preguntas realizadas:

Durante la depuración fui proporcionando los errores y partes del código a la IA para identificar qué estaba fallando.

Preguntaba de dónde venía determinado error, qué archivo debía modificarse, si el problema estaba en la llamada entre clases o si existía una incompatibilidad entre los datos que se estaban enviando.

También fui utilizando la IA para revisar los cambios antes de volver a ejecutar las pruebas.

## Sugerencia recibida:

La IA me ayudó a seguir las referencias entre archivos y a identificar qué partes tenían que cambiarse juntas.

En lugar de modificar únicamente el archivo donde aparecía el error, se revisaba el recorrido completo de la información para encontrar dónde se originaba realmente el problema.

## Decisión tomada:

Decidí utilizar la IA como una herramienta de depuración y no solamente como una herramienta para escribir código.

Cuando tenía una idea de cómo resolver algo, primero se la explicaba y revisábamos si tenía sentido. Después la implementaba, ejecutaba las pruebas y, si aparecía un error, utilizábamos ese resultado para continuar corrigiendo.

Este proceso se repitió varias veces hasta conseguir que todo funcionara correctamente.

## Cambios realizados:

Durante esta jornada se corrigieron diferentes relaciones entre modelos, repositorios, servicios, esquemas, routers y pruebas.

También se agregaron validaciones para sensores y lecturas, se modificaron las llamadas de la API y se actualizaron las pruebas para comprobar los nuevos comportamientos.

Después de realizar los cambios se ejecutaron las herramientas de revisión:

* Ruff.
* Mypy.
* Pytest.

El resultado final fue:

* Ruff: todos los checks pasaron.
* Mypy: sin errores.
* Pytest: **58 pruebas aprobadas**.
* Cobertura total: **87.66%**.

## Resultado:

Después de varias horas de correcciones y pruebas, el proyecto quedó funcionando correctamente y los cambios principales pudieron ser guardados en un commit.

El commit realizado fue:

`4be601f – feat: add sensor and reading validation`

Esta parte del trabajo me permitió entender que modificar un proyecto que ya tiene varias partes conectadas no consiste únicamente en cambiar el archivo donde quiero agregar algo. También tengo que revisar las relaciones entre las diferentes partes del sistema y comprobar que los cambios no rompan funcionalidades existentes.

---

# Reflexión final

Durante esta etapa entendí mejor el uso que quiero darle a la inteligencia artificial durante mi aprendizaje y desarrollo.

No la estoy utilizando solamente para que escriba código por mí. Principalmente me sirve para **organizar mis ideas, planificar el proyecto, entender conceptos que todavía no comprendo, buscar formas de aprenderlos y acelerar mi producción**.

Cuando tengo una idea, puedo explicársela a la IA y preguntarle si tiene sentido, cómo podría implementarse y qué problemas podrían aparecer. Después puedo llevar esa idea al código y comprobar realmente si funciona.

Si aparecen errores, la IA también me ayuda a analizarlos y encontrar dónde puede estar el problema. De esta manera puedo dedicar menos tiempo a intentar descubrir desde cero dónde está cada error y más tiempo a entender qué está pasando y aprender de la solución.

También entendí que la IA no siempre tiene que darme directamente la respuesta final. Muchas veces me sirve más como una herramienta para organizar el problema y explicarme el razonamiento detrás de una solución.

En esta etapa, la IA me ayudó a avanzar más rápido, pero las decisiones finales y los cambios realizados en el proyecto fueron revisados por mí y comprobados mediante las pruebas del sistema.
