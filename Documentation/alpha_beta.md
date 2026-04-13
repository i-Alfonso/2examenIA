# Alpha-Beta

## Objetivo

Se agrego `AI/alpha_beta.py` para implementar poda alfa-beta reutilizable.

Este modulo elige la direccion de Pinky usando el modelo de estados del grafo. La conexion con el juego visual se hace desde `AI/ghost_controller.py` y `Ghost.py`.

## Archivo Agregado

```text
AI/alpha_beta.py
```

## Idea Principal

El juego se mueve en tiempo real, pero la busqueda se modela por turnos.

Para Pinky:

```text
MAX = Pinky
MIN = PacMan
```

Pinky intenta maximizar el score de la funcion de evaluacion.

PacMan intenta minimizar ese score, simulando que busca escapar.

Para Inky/Clyde:

```text
MAX = Inky y Clyde como pareja
MIN = PacMan
```

La accion MAX ya no es una sola direccion, sino una tupla:

```text
(direccion_inky, direccion_clyde)
```

## Profundidad Recomendada

Para Pinky se recomienda iniciar con:

```python
depth = 4
```

Eso representa:

```text
Pinky mueve
PacMan responde
Pinky mueve
PacMan responde
```

Si el rendimiento es bueno, se puede probar con:

```text
depth = 5 o 6
```

Para Inky/Clyde se recomienda iniciar con:

```python
depth = 3
```

La profundidad es menor porque cada turno de fantasmas genera combinaciones de movimientos de dos agentes.

## Funciones Agregadas

### SearchStats

Guarda metricas de la busqueda.

```python
SearchStats(
    nodes_expanded=0,
    leaves_evaluated=0,
    alpha_cuts=0,
    beta_cuts=0,
    max_depth_reached=0,
)
```

Estas metricas sirven para el reporte:

- nodos expandidos,
- hojas evaluadas,
- cortes alfa,
- cortes beta,
- profundidad alcanzada.

### is_capture_state

Revisa si un fantasma esta en el mismo nodo que PacMan.

```python
is_capture_state(state, ghost_index=0)
```

Si devuelve `True`, la busqueda puede detenerse porque se encontro captura.

### order_children

Ordena los hijos antes de buscarlos.

```python
order_children(children, evaluate, maximizing)
```

Esto es una mejora de rendimiento porque alfa-beta poda mejor cuando revisa primero los movimientos prometedores.

### alpha_beta

Implementa la recursion principal.

```python
alpha_beta(
    state,
    depth,
    alpha,
    beta,
    maximizing,
    generate_children,
    evaluate,
)
```

Es generico porque no depende directamente de Pinky. Recibe funciones externas:

```text
generate_children
evaluate
is_terminal
```

### choose_best_action

Evalua los hijos del estado raiz y devuelve:

```python
best_action, best_value, stats
```

Esto permite saber:

```text
que direccion tomar
que valor obtuvo
cuantas ramas se exploraron
```

### generate_pinky_alpha_beta_children

Genera hijos alternando entre:

```text
turno ghosts -> mueve Pinky
turno pacman -> mueve PacMan
```

Usa:

```python
generate_single_ghost_children
generate_pacman_children
```

### choose_pinky_action

Funcion lista para elegir la direccion de Pinky.

```python
choose_pinky_action(graph, state, depth=4, tabu_horizon=4)
```

Devuelve:

```python
best_action, best_value, stats
```

Donde `best_action` es una direccion:

```text
0 = arriba
1 = derecha
2 = abajo
3 = izquierda
```

### generate_pack_alpha_beta_children

Genera hijos alternando entre:

```text
turno ghosts -> mueven Inky y Clyde juntos
turno pacman -> mueve PacMan
```

Usa:

```python
generate_joint_ghost_children
generate_pacman_children
```

### choose_pack_action

Funcion lista para elegir la accion conjunta de Inky y Clyde.

```python
choose_pack_action(graph, state, depth=3, tabu_horizon=4)
```

Devuelve:

```python
best_action, best_value, stats
```

Donde `best_action` es:

```text
(direccion_inky, direccion_clyde)
```

## Mejoras Incluidas

### Ordenamiento De Movimientos

Antes de buscar, los hijos se ordenan usando la funcion de evaluacion.

Esto ayuda a que alfa-beta encuentre buenas ramas antes y pueda podar mas.

### Corte Por Captura

Si Pinky alcanza el mismo nodo que PacMan, la rama se detiene como estado terminal.

### Tabu Con Horizonte Limitado

Cada movimiento simulado de Pinky agrega el nuevo nodo al historial tabu.

El horizonte actual recomendado es:

```python
tabu_horizon = 4
```

Esto significa que la busqueda recuerda solo los ultimos 4 nodos/estados relevantes.

El tabu se aplica como penalizacion, no como prohibicion absoluta. Esto evita bloquear al fantasma en pasillos o intersecciones con pocas salidas.

## Relacion Con La Heuristica

Para Pinky, alfa-beta usa:

```python
evaluate_pinky_state(graph, state)
```

Esa evaluacion considera:

- distancia real a PacMan,
- rutas de escape de PacMan,
- penalizacion tabu con horizonte limitado.

Para Inky/Clyde, alfa-beta usa:

```python
evaluate_pack_state(graph, state)
```

Esa evaluacion considera:

- distancia de ambos fantasmas a PacMan,
- salidas cubiertas,
- rutas libres,
- separacion util,
- solapamiento de salida,
- penalizacion tabu.

## Estado Actual

Pinky ya esta conectado al juego:

```text
main.py -> PinkyGhostController -> choose_pinky_action -> alpha_beta
```

El segundo fantasma (`ghosts[1]`) usa alfa-beta cuando llega a una interseccion.

Inky y Clyde (`ghosts[2]` y `ghosts[3]`) usan alfa-beta colaborativo mediante `PackGhostController`.

## Lo Que Sigue

El siguiente paso es probar visualmente y ajustar pesos:

```text
DEFAULT_PACK_COVERAGE_DISTANCE
pesos de cobertura
pesos de rutas libres
profundidad de busqueda
```
