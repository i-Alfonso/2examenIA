# Collaborative Decision Timing

## Objetivo

Este documento explica cuando se toma la foto de Inky/Clyde, cuando se ejecuta alfa-beta colaborativo y que pasa si uno de los fantasmas esta en una interseccion mientras el otro esta en un pasillo.

Este detalle es importante porque el juego visual se mueve por pixeles, pero la IA decide sobre intersecciones.

## Resumen Corto

```text
La foto de Inky/Clyde se actualiza cada frame.
La decision de alfa-beta solo se pide cuando un fantasma llega a una interseccion.
Un fantasma en pasillo no cambia de direccion; sigue recto.
```

La foto por frame no viola la regla del proyecto porque guardar posiciones no es tomar una decision. La decision real se aplica solo en intersecciones.

## Flujo Real En main.py

En cada frame, `display()` guarda una foto de los dos fantasmas colaborativos y de PacMan:

```python
pack_controller.set_pack_snapshot(
    ghosts[2].position,
    ghosts[2].direction,
    ghosts[3].position,
    ghosts[3].direction,
    pc.position,
    pc.direction,
)
```

Despues actualiza los fantasmas:

```python
for g in ghosts:
    g.draw()
    g.update2(pc.position, pc.direction)
```

La foto contiene:

```text
posicion de Inky
direccion de Inky
posicion de Clyde
direccion de Clyde
posicion de PacMan
direccion de PacMan
```

## Flujo Real En Ghost.update2()

`Ghost.update2()` decide si el fantasma puede consultar IA:

```text
si esta en interseccion:
    si es fantasma inteligente:
        pedir direccion al controlador
    si no:
        elegir movimiento aleatorio
si no esta en interseccion:
    seguir adelante
```

Por eso, aunque `main.py` actualice la foto cada frame, un fantasma en pasillo no pide alfa-beta.

## Por Que La Foto Es Cada Frame

La foto solo copia posiciones y direcciones actuales.

Es barato y evita problemas de orden:

```text
1. Se guarda la posicion actual de Inky y Clyde.
2. Inky puede decidir usando esa misma foto.
3. Clyde puede decidir usando esa misma foto.
```

Si la foto no existiera, podria pasar:

```text
Inky se mueve primero.
Clyde decide despues usando la posicion ya modificada de Inky.
```

Eso haria que ambos no estuvieran decidiendo sobre el mismo estado.

## Caso 1: Ambos Estan En Interseccion

Este es el caso ideal.

Flujo:

```text
1. main.py guarda la foto de ambos.
2. Inky llega a update2().
3. Inky pide direccion al PackGhostController.
4. El controlador ejecuta alfa-beta colaborativo.
5. Alfa-beta devuelve:
   (direccion_inky, direccion_clyde)
6. Inky aplica direccion_inky.
7. Clyde llega a update2().
8. Clyde pide direccion.
9. El controlador reutiliza la misma decision cacheada.
10. Clyde aplica direccion_clyde.
```

Resultado:

```text
ambos usan la misma decision conjunta calculada desde la misma foto.
```

## Caso 2: Inky En Interseccion, Clyde En Pasillo

Flujo:

```text
1. main.py guarda la foto actual de Inky, Clyde y PacMan.
2. Inky esta en interseccion.
3. Inky pide decision al PackGhostController.
4. El controlador construye un estado usando:
   - Inky en su interseccion actual,
   - Clyde aproximado a la interseccion mas cercana,
   - PacMan aproximado a la interseccion mas cercana.
5. Alfa-beta devuelve una accion conjunta.
6. Inky aplica su direccion.
7. Clyde no aplica la suya porque esta en pasillo.
8. Clyde sigue recto con `sigue_adelante()`.
```

Resultado:

```text
Inky usa una decision cooperativa considerando a Clyde.
Clyde no cambia direccion hasta llegar a una interseccion.
```

Esto respeta la regla del proyecto porque Clyde no decide en pasillo.

## Caso 3: Clyde En Interseccion, Inky En Pasillo

Es el mismo caso invertido.

Flujo:

```text
1. main.py guarda la foto actual.
2. Clyde esta en interseccion.
3. Clyde pide decision al PackGhostController.
4. El controlador aproxima a Inky al nodo mas cercano.
5. Alfa-beta devuelve una accion conjunta.
6. Clyde aplica su direccion.
7. Inky sigue recto porque esta en pasillo.
```

Resultado:

```text
Clyde toma la decision cooperativa disponible.
Inky conserva su movimiento hasta su siguiente interseccion.
```

## Caso 4: Ninguno Esta En Interseccion

Flujo:

```text
1. main.py guarda la foto.
2. Inky no esta en interseccion.
3. Inky sigue adelante.
4. Clyde no esta en interseccion.
5. Clyde sigue adelante.
```

Resultado:

```text
no se ejecuta alfa-beta colaborativo.
ambos conservan su direccion.
```

## Caso 5: Uno Llega A Interseccion Justo Despues De Que El Otro Se Movio

El orden del loop actualiza fantasmas uno por uno.

La foto se tomo antes de actualizar a cualquiera, por eso la decision colaborativa usa el estado inicial del frame.

Ejemplo:

```text
foto inicial del frame:
  Inky = A
  Clyde = B

se actualiza Inky
se actualiza Clyde
```

Si Clyde decide en ese frame, decide con la foto inicial, no con una foto donde Inky ya se movio.

Esto mantiene sincronizada la decision.

## Caso 6: Un Fantasma Esta En Pasillo Y Se Aproxima Al Nodo Mas Cercano

`PackGhostController.build_state()` usa:

```python
require_exact=False
```

para Inky, Clyde y PacMan.

Eso significa:

```text
si el actor no esta exactamente en una interseccion,
se usa la interseccion mas cercana.
```

Esto es una aproximacion necesaria porque alfa-beta trabaja con nodos de `MC`, no con cada pixel del pasillo.

La aproximacion no autoriza al fantasma a girar en pasillo. Solo sirve para evaluar el estado cooperativo.

## Caso 7: La Accion Calculada No Es Valida Para El Fantasma Actual

Cuando `Ghost.path_ia()` recibe una direccion del controlador, todavia valida:

```python
self.can_move_direction(next_direction)
```

Si la direccion no se puede ejecutar:

```text
se usa `interseccion_random()` como respaldo.
```

Esto evita que una accion de IA saque al fantasma del tablero o lo mande por un pasillo invalido.

## Caso 8: PacMan Esta En Pasillo

PacMan tambien puede no estar exactamente en una interseccion.

Para construir el estado de busqueda, el controlador aproxima PacMan al nodo mas cercano:

```python
actor_from_position(..., require_exact=False)
```

Esto mantiene el modelo simple:

```text
la busqueda decide sobre intersecciones,
no sobre cada pixel del recorrido.
```

## Por Que No Tomar Foto Solo En Intersecciones

Se podria hacer, pero no cambia la regla importante.

Lo costoso no es:

```text
guardar la foto
```

Lo costoso es:

```text
ejecutar alfa-beta
```

Y alfa-beta solo se ejecuta cuando un fantasma inteligente llega a interseccion y pide direccion.

Guardar la foto cada frame tiene ventajas:

- mantiene datos recientes,
- simplifica el orden de actualizacion,
- evita decisiones calculadas con estados mezclados,
- no cambia direcciones en pasillos.

## Respuesta Recomendada Para El Profesor

```text
En cada frame guardamos una foto de Inky, Clyde y PacMan para tener un estado sincronizado. Sin embargo, alfa-beta no se aplica en cada frame. Cada fantasma solo pide decision cuando esta en una interseccion. Si uno esta en interseccion y el otro esta en pasillo, el que esta en interseccion decide usando una aproximacion del otro al nodo mas cercano; el que esta en pasillo sigue recto hasta su siguiente interseccion. Asi se respeta la regla de movimiento y se mantiene la colaboracion.
```
