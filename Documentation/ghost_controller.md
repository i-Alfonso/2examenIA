# Ghost Controller

## Objetivo

Se agrego `AI/ghost_controller.py` para conectar la IA con los fantasmas del juego.

La idea es que `Ghost.py` no contenga la implementacion de alfa-beta. El fantasma solo pregunta al controlador que direccion debe tomar cuando llega a una interseccion.

## Archivo Agregado

```text
AI/ghost_controller.py
```

## Cambios En El Proyecto

Se actualizo:

```text
Ghost.py
main.py
AI/__init__.py
```

## PinkyGhostController

La clase principal es:

```python
PinkyGhostController
```

Se crea con:

```python
pinky_controller = PinkyGhostController(maze_graph, depth=4, tabu_horizon=4)
```

Donde:

```text
maze_graph
  grafo de intersecciones del laberinto.

depth
  profundidad de busqueda para alfa-beta.

tabu_horizon
  cuantos nodos recientes se recuerdan para penalizar ciclos.
```

## Funcionamiento

Cuando Pinky llega a una interseccion:

```text
1. Ghost.py llama al controlador.
2. El controlador convierte posiciones reales a nodos del grafo.
3. Crea un GameState.
4. Ejecuta choose_pinky_action().
5. Devuelve una direccion.
6. Ghost.py mueve a Pinky en esa direccion.
```

## build_state

Construye el estado de busqueda.

```python
build_state(
    ghost_position,
    ghost_direction,
    pacman_position,
    pacman_direction,
)
```

Pinky debe estar exactamente en una interseccion porque solo decide en intersecciones.

PacMan puede estar en un pasillo, por eso se usa el nodo mas cercano cuando no esta exactamente en una interseccion.

## next_direction

Pide a alfa-beta la siguiente direccion.

```python
next_direction(
    ghost_position,
    ghost_direction,
    pacman_position,
    pacman_direction,
)
```

Devuelve:

```text
0 = arriba
1 = derecha
2 = abajo
3 = izquierda
None = no se pudo decidir
```

Si no se puede decidir, `Ghost.py` usa movimiento aleatorio como respaldo.

## PackGhostController

La clase colaborativa es:

```python
PackGhostController
```

Se crea con:

```python
pack_controller = PackGhostController(maze_graph, depth=3, tabu_horizon=4)
```

Este controlador decide para dos fantasmas al mismo tiempo:

```text
ghosts[2] = Inky
ghosts[3] = Clyde
```

Antes de actualizar los fantasmas, `main.py` toma una foto de sus posiciones:

```python
pack_controller.set_pack_snapshot(...)
```

Luego cada fantasma pregunta su direccion. El controlador calcula una sola accion conjunta:

```text
(direccion_inky, direccion_clyde)
```

y devuelve a cada fantasma la direccion que le corresponde.

Esto evita que Inky decida con una posicion y Clyde decida con otra posicion ya modificada.

## Cambios En Ghost.py

Se agrego:

```python
setController(controller, ghost_index=None)
```

`ghost_index` se usa para saber si el fantasma representa a Inky (`0`) o Clyde (`1`) dentro del controlador colaborativo.

Tambien se agrego:

```python
move_direction(direction)
```

para evitar duplicar el codigo que mueve al fantasma segun una direccion.

Tambien se agregaron validaciones de borde:

```python
is_inside_board_position(x, z)
next_pixel_for_direction(direction)
can_move_direction(direction)
```

Estas funciones evitan que un fantasma pueda moverse a un pixel fuera del tablero. Antes, si un controlador o el respaldo aleatorio intentaban mover hacia arriba estando en el borde superior, el fantasma podia salir visualmente del mapa.

Ahora `move_direction()` regresa `False` si la direccion sacaria al fantasma del rango valido.

Cuando `tipo == 1`, el fantasma usa:

```python
path_ia(pacmanXY, pacman_dir)
```

Ese metodo llama al controlador.

## Cambios En main.py

Se agrego:

```python
from AI import MazeGraph, PackGhostController, PinkyGhostController
```

Se crea el grafo:

```python
maze_graph = MazeGraph(MC, xMC, yMC)
```

Se crea el controlador:

```python
pinky_controller = PinkyGhostController(maze_graph, depth=4, tabu_horizon=4)
pack_controller = PackGhostController(maze_graph, depth=3, tabu_horizon=4)
```

El segundo fantasma se configura como Pinky inteligente:

```python
ghosts.append(Ghost(..., 378, 20, 0, 1))
ghosts[1].setController(pinky_controller)
```

Esto deja el reparto asi:

```text
ghosts[0] = Blinky aleatorio
ghosts[1] = Pinky con alfa-beta
ghosts[2] = Inky con alfa-beta colaborativo
ghosts[3] = Clyde con alfa-beta colaborativo
```

## Logs De IA En Consola

Se agregaron logs controlados por:

```python
DEBUG_AI_LOGS = True
AI_LOG_INTERVAL_FRAMES = 60
```

Cuando `DEBUG_AI_LOGS` esta activo, cada 60 frames se imprime:

```text
[AI][State]
[AI][Pinky]
[AI][Pack]
```

`[AI][State]` muestra posiciones y direcciones actuales.

`[AI][Pinky]` muestra:

```text
accion elegida
valor de alfa-beta
nodos expandidos
hojas evaluadas
cortes alfa/beta
componentes heuristicos
```

`[AI][Pack]` muestra lo mismo para la decision conjunta de Inky y Clyde.

Estos logs sirven para comprobar si los fantasmas estan usando alfa-beta o si hay que ajustar pesos/profundidad.

## Mapeo De Colores

Los archivos BMP del proyecto no estan en el mismo orden que los nombres clasicos de PacMan.

El mapeo correcto observado es:

```text
fantasma1.bmp = naranja = Clyde
fantasma2.bmp = azul/cian = Inky
fantasma3.bmp = rosa = Pinky
fantasma4.bmp = rojo = Blinky
```

Por eso en `main.py` se usan nombres semanticos:

```python
img_blinky = fantasma4.bmp
img_pinky = fantasma3.bmp
img_inky = fantasma2.bmp
img_clyde = fantasma1.bmp
```

Actualmente se muestran los cuatro fantasmas:

```text
Blinky rojo = aleatorio
Pinky rosa = alfa-beta
Inky azul/cian = alfa-beta colaborativo
Clyde naranja = alfa-beta colaborativo
```

## Lo Que Sigue

Despues de conectar Pinky e Inky/Clyde, el siguiente paso es probar visualmente y ajustar:

```text
pesos de la heuristica colaborativa
profundidad de alfa-beta
metricas visibles o logs de prueba
```

El tabu de Pinky ya quedo integrado en `GameState`, `alpha_beta` y `heuristics`. No se creo un archivo separado porque por ahora la memoria tabu es pequena y se guarda directamente dentro de cada estado simulado.
