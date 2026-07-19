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




