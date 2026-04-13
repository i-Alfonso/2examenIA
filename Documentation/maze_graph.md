# Maze Graph

## Objetivo

Se agrego el modulo `AI/maze_graph.py` para representar el laberinto como un grafo de intersecciones.

La idea principal es conservar el movimiento visual por pixeles, pero hacer que la IA tome decisiones solo en intersecciones. Esto evita que alfa-beta tenga que analizar una accion nueva en cada pixel del pasillo.

## Archivos Agregados

```text
AI/__init__.py
AI/maze_graph.py
```

## Por Que Usar Un Grafo

El proyecto base ya contiene la informacion necesaria para saber donde estan las intersecciones:

```text
MC
xMC
yMC
mapa.csv
mapa_codigos.csv
```

El nuevo modulo no reemplaza esa informacion. La organiza en una estructura mas facil de usar para busqueda.

Antes:

```text
estoy en una coordenada -> consulto MC -> saco direcciones posibles
```

Ahora tambien podemos hacer:

```text
estoy en un nodo -> consulto vecinos -> simulo futuros movimientos -> evaluo con alfa-beta
```

## Representacion

Cada nodo del grafo es una interseccion real de `MC`.

Un nodo se representa como:

```python
(row, col)
```

Ejemplo:

```python
(0, 0)
```

Ese nodo corresponde a la primera interseccion de la matriz de control.

Cada arista contiene:

```python
target
direction
cost
```

Ejemplo conceptual:

```python
Edge(target=(0, 2), direction=1, cost=71)
```

Esto significa:

```text
desde el nodo actual, ir a la derecha llega al nodo (0, 2) y cuesta 71 pixeles
```

## Direcciones

El proyecto usa los mismos codigos que `Pacman.py` y `Ghost.py`:

```text
0 = arriba
1 = derecha
2 = abajo
3 = izquierda
```

## Clase Principal

La clase principal es:

```python
MazeGraph
```

Uso esperado:

```python
from AI.maze_graph import MazeGraph

maze_graph = MazeGraph(MC, xMC, yMC)
```

## Metodos Principales

### get_neighbors(node)

Devuelve las aristas disponibles desde un nodo.

```python
maze_graph.get_neighbors((0, 0))
```

Resultado esperado:

```text
derecha hacia otro nodo
abajo hacia otro nodo
```

### next_node(node, direction)

Devuelve la arista que se alcanza si se toma una direccion.

```python
maze_graph.next_node((0, 0), 1)
```

### get_cost(origin, destination)

Devuelve el costo entre dos nodos vecinos.

```python
maze_graph.get_cost((0, 0), (0, 2))
```

### direction_between(origin, destination)

Devuelve que direccion conecta dos nodos vecinos.

```python
maze_graph.direction_between((0, 0), (0, 2))
```

### node_to_pixel(node)

Convierte un nodo del grafo a coordenadas usadas por el juego.

```python
maze_graph.node_to_pixel((0, 0))
```

Resultado:

```python
(20, 20)
```

### pixel_to_node(x, z)

Convierte una coordenada del juego a nodo si la posicion cae exactamente en una interseccion.

```python
maze_graph.pixel_to_node(20, 20)
```

Resultado:

```python
(0, 0)
```

### shortest_distance(origin, destination)

Calcula la distancia real por pasillos usando Dijkstra.

```python
maze_graph.shortest_distance((0, 0), (9, 9))
```

Esta distancia sirve para las heuristicas de los fantasmas.

## Por Que Dijkstra

Dijkstra no reemplaza alfa-beta.

Dijkstra solo calcula distancias reales dentro del laberinto.

Alfa-beta usara esas distancias para evaluar estados.

Ejemplo:

```text
Pinky simula tres posibles movimientos.
Para cada movimiento, se calcula que tan lejos queda de PacMan.
La distancia se calcula por el grafo, no en linea recta.
Alfa-beta elige el movimiento con mejor evaluacion.
```

Esto es mejor que usar distancia euclidiana porque el laberinto tiene paredes.

## Validaciones Esperadas

Con los datos actuales del proyecto, el grafo debe cumplir:

```text
66 nodos
170 aristas dirigidas
conectividad completa
0 aristas asimetricas
```

El modulo incluye:

```python
validate(expected_nodes=66, expected_edges=170)
```

Ese metodo devuelve un diccionario con el estado de la validacion.

## Relacion Con Alfa-Beta

Este modulo es la base para generar hijos en alfa-beta.

Para Pinky:

```text
estado actual de Pinky -> vecinos posibles -> estados hijos -> evaluacion
```

Para Inky y Clyde:

```text
estado conjunto -> combinaciones de vecinos -> estados hijos colaborativos -> evaluacion compartida
```

## Lo Que Sigue

Despues de este modulo, el siguiente paso es crear:

```text
AI/game_state.py
```

Ese archivo debe representar:

```text
posicion de PacMan
direccion de PacMan
posicion de Pinky
direccion de Pinky
posiciones de Inky y Clyde
direcciones de Inky y Clyde
turno actual
historial tabu
```

Luego se puede implementar:

```text
AI/alpha_beta.py
AI/heuristics.py
AI/tabu.py
AI/ghost_controller.py
```
