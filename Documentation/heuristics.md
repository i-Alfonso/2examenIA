# Heuristics

## Objetivo

Se agrego `AI/heuristics.py` para definir funciones de evaluacion que puedan usar los fantasmas con poda alfa-beta.

La primera funcion implementada es para Pinky, el fantasma rosa que debe perseguir a PacMan usando alfa-beta individual.

## Archivo Agregado

```text
AI/heuristics.py
```

## Idea Principal

Alfa-beta necesita una forma de decidir si un estado es bueno o malo.

Para Pinky, un estado es mejor cuando:

- Pinky esta mas cerca de PacMan por caminos reales del laberinto.
- PacMan tiene menos rutas de escape desde su interseccion.
- Pinky evita repetir estados/nodos recientes cuando se use tabu.

La funcion de evaluacion devuelve un numero:

```text
score alto = mejor para Pinky
score bajo = peor para Pinky
```

## Componentes Heuristicos De Pinky

### 1. Distancia Real A PacMan

Se calcula con:

```python
distance_to_pacman(graph, state, ghost_index=0)
```

Esta funcion usa:

```python
graph.shortest_distance(...)
```

Por lo tanto, mide distancia real por pasillos usando Dijkstra.

No usa distancia en linea recta porque el laberinto tiene paredes.

Ejemplo:

```text
Pinky puede estar visualmente cerca de PacMan,
pero si hay una pared en medio, la distancia real puede ser grande.
```

Este componente se usa de forma negativa:

```text
menor distancia = mejor score
mayor distancia = peor score
```

### 2. Rutas De Escape De PacMan

Se calcula con:

```python
pacman_escape_routes(graph, state)
```

Cuenta cuantas direcciones legales tiene PacMan desde su nodo actual.

Ejemplo:

```text
PacMan en un cruce de 4 caminos = muchas rutas de escape
PacMan en una esquina = pocas rutas de escape
```

Para Pinky, es mejor que PacMan tenga pocas salidas.

Por eso este componente tambien se penaliza:

```text
mas rutas de escape = peor score para Pinky
menos rutas de escape = mejor score para Pinky
```

### 3. Penalizacion Tabu

Se calcula con:

```python
tabu_penalty(state, ghost_index=0)
```

Esta parte queda preparada para cuando se implemente tabu con horizonte limitado.

La idea es penalizar estados donde Pinky vuelva a nodos recientes.

Esto ayuda a evitar ciclos como:

```text
ir derecha
regresar izquierda
ir derecha
regresar izquierda
```

## Funcion Principal

La funcion principal es:

```python
evaluate_pinky_state(graph, state, ghost_index=0)
```

Formula conceptual:

```text
score =
  - distancia_real_a_PacMan
  - peso_escape * rutas_de_escape_de_PacMan
  - peso_tabu * penalizacion_tabu
```

Valores actuales:

```python
DEFAULT_DISTANCE_WEIGHT = 1.0
DEFAULT_ESCAPE_ROUTE_WEIGHT = 12.0
DEFAULT_TABU_WEIGHT = 25.0
CAPTURE_SCORE = 10000.0
```

Si Pinky llega al mismo nodo que PacMan, se devuelve:

```python
CAPTURE_SCORE
```

Eso representa captura.

## Por Que Cumple Con El Inciso De Pinky

El PDF pide:

```text
Definir una funcion de evaluacion para alfa-beta con al menos dos componentes heuristicos.
```

Esta evaluacion tiene al menos dos componentes principales:

```text
1. distancia real por el laberinto entre Pinky y PacMan
2. numero de rutas de escape de PacMan
```

Ademas deja preparado:

```text
3. penalizacion tabu
```

La funcion todavia no mueve a Pinky por si sola. Su objetivo es evaluar estados. La decision final se hara cuando se implemente `AI/alpha_beta.py`.

## Funciones Agregadas

### resolve_node

Permite usar tanto un `ActorState` como un nodo directo.

```python
resolve_node(actor_or_node)
```

### graph_distance

Calcula distancia real entre dos actores o nodos.

```python
graph_distance(graph, origin, destination)
```

### distance_to_pacman

Calcula distancia real entre un fantasma y PacMan.

```python
distance_to_pacman(graph, state, ghost_index=0)
```

### pacman_escape_routes

Cuenta las salidas legales de PacMan.

```python
pacman_escape_routes(graph, state)
```

### tabu_penalty

Penaliza si el fantasma cae en un nodo marcado como tabu.

```python
tabu_penalty(state, ghost_index=0)
```

### pinky_heuristic_components

Devuelve las partes de la evaluacion por separado.

```python
pinky_heuristic_components(graph, state)
```

Esto sirve para imprimir, depurar y explicar en el reporte.

### evaluate_pinky_state

Devuelve el score final para Pinky.

```python
evaluate_pinky_state(graph, state)
```

## Lo Que Sigue

Despues de esta heuristica, el siguiente paso es implementar:

```text
AI/alpha_beta.py
```

Ese archivo debe usar:

```text
GameState
generate_single_ghost_children
generate_pacman_children
evaluate_pinky_state
```

para elegir la mejor direccion de Pinky.
