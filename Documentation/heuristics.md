# Heuristics

## Objetivo

Se agrego `IA/heuristics.py` para definir funciones de evaluacion que puedan usar los fantasmas con poda alfa-beta.

Primero se implemento Pinky, el fantasma rosa que persigue a PacMan usando alfa-beta individual.

Despues se agrego la evaluacion colaborativa para Inky y Clyde, cuyo objetivo no es solo acercarse a PacMan, sino reducir sus rutas de escape.

## Archivo Agregado

```text
IA/heuristics.py
```

## Idea Principal

Alfa-beta necesita una forma de decidir si un estado es bueno o malo.

Para Pinky, un estado es mejor cuando:

- Pinky esta mas cerca de PacMan segun una distancia heuristica.
- PacMan tiene menos rutas de escape desde su interseccion.
- Pinky evita repetir estados/nodos recientes cuando se use tabu.

La funcion de evaluacion devuelve un numero:

```text
score alto = mejor para Pinky
score bajo = peor para Pinky
```

## Componentes Heuristicos De Pinky

### 1. Distancia Heuristica A PacMan

Se calcula con:

```python
distance_to_pacman(maze, state, ghost_index=0)
```

Esta funcion usa por defecto:

```python
manhattan_distance(...)
```

La distancia configurada por defecto es Manhattan:

```text
abs(x1 - x2) + abs(y1 - y2)
```

No se usa camino minimo ni pathfinding.

La razon es que alfa-beta debe decidir con simulacion adversarial. La distancia solo es una estimacion de cercania entre nodos.

Este componente se usa de forma negativa:

```text
menor distancia = mejor score
mayor distancia = peor score
```

### 2. Rutas De Escape De PacMan

Se calcula con:

```python
pacman_escape_routes(maze, state)
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

Esta parte aplica tabu con horizonte limitado cuando los estados hijos agregan nodos recientes al historial.

La idea es penalizar estados donde Pinky vuelva a nodos recientes.

Esto ayuda a evitar ciclos como:

```text
ir derecha
regresar izquierda
ir derecha
regresar izquierda
```

## Funcion Principal De Pinky

La funcion principal es:

```python
evaluate_pinky_state(maze, state, ghost_index=0)
```

Formula conceptual:

```text
score =
  - distancia_heuristica_a_PacMan
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
1. distancia Manhattan entre Pinky y PacMan
2. numero de rutas de escape de PacMan
```

Ademas incluye:

```text
3. penalizacion tabu
```

La decision final de Pinky se toma desde `IA/alpha_beta.py` con `choose_pinky_action()`.

## Componentes Heuristicos De Inky/Clyde

Para los dos fantasmas colaborativos se agrego:

```python
evaluate_pack_state(maze, state)
```

Esta funcion evalua un estado donde `state.ghosts` contiene dos fantasmas:

```text
ghosts[0] = Inky
ghosts[1] = Clyde
```

La idea es premiar estados donde PacMan quede con menos salidas utiles.

Componentes:

```text
distancia total heuristica de Inky/Clyde a PacMan
distancia del fantasma mas cercano a PacMan
rutas de escape de PacMan
salidas cubiertas por algun fantasma
rutas libres de PacMan
separacion util entre Inky y Clyde
penalizacion si ambos cubren la misma salida
penalizacion tabu
```

### Salidas Cubiertas

Se calcula con:

```python
pacman_exit_coverage(maze, state)
```

Por cada salida de PacMan, se revisa si Inky o Clyde estan cerca de esa salida. Si alguno esta dentro del rango definido por `DEFAULT_PACK_COVERAGE_DISTANCE`, esa salida cuenta como cubierta.

Esto evita que ambos fantasmas persigan por el mismo pasillo sin cerrar otras rutas.

### Separacion Util

Se calcula con:

```python
useful_separation_score(maze, state)
```

La separacion se evalua asi:

```text
demasiado juntos = malo
separacion media = bueno
demasiado lejos = neutro
```

### Solapamiento De Salidas

Se calcula con:

```python
exit_overlap_penalty(maze, state)
```

Penaliza cuando Inky y Clyde estan cubriendo la misma salida principal de PacMan. Eso ayuda a que trabajen en rutas distintas.

## Funcion Principal De Inky/Clyde

Formula conceptual:

```text
score =
  - distancia_total_a_PacMan
  - distancia_minima_a_PacMan
  - rutas_escape_PacMan
  + salidas_cubiertas
  - rutas_libres
  + separacion_util
  - solapamiento
  - tabu
```

Mientras mayor sea el score, mejor es el encierro.

## Funciones Agregadas

### resolve_node

Permite usar tanto un `ActorState` como un nodo directo.

```python
resolve_node(actor_or_node)
```

### manhattan_distance

Calcula la distancia heuristica entre dos actores o nodos.

```python
manhattan_distance(maze, origin, destination)
```

Por defecto usa Manhattan y no hace busqueda de camino minimo.

### distance_to_pacman

Calcula distancia heuristica entre un fantasma y PacMan.

```python
distance_to_pacman(maze, state, ghost_index=0)
```

### pacman_escape_routes

Cuenta las salidas legales de PacMan.

```python
pacman_escape_routes(maze, state)
```

### tabu_penalty

Penaliza si el fantasma cae en un nodo marcado como tabu.

```python
tabu_penalty(state, ghost_index=0)
```

### pinky_heuristic_components

Devuelve las partes de la evaluacion por separado.

```python
pinky_heuristic_components(maze, state)
```

Esto sirve para imprimir, depurar y explicar en el reporte.

### evaluate_pinky_state

Devuelve el score final para Pinky.

```python
evaluate_pinky_state(maze, state)
```

### pack_heuristic_components

Devuelve las partes de la evaluacion colaborativa.

```python
pack_heuristic_components(maze, state)
```

### evaluate_pack_state

Devuelve el score final para Inky/Clyde.

```python
evaluate_pack_state(maze, state)
```

## Lo Que Sigue

Despues de estas heuristicas, el siguiente paso es probar visualmente:

```text
Pinky persiguiendo con alfa-beta
Inky/Clyde intentando reducir salidas de PacMan
```
