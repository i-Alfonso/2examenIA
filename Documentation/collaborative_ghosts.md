# Fantasmas Colaborativos

## Objetivo

Se agrego la IA colaborativa para Inky y Clyde.

La meta no es que ambos fantasmas sigan exactamente el mismo camino hacia PacMan. La meta es que trabajen como pareja para reducir sus rutas de escape.

## Archivos Modificados

```text
AI/heuristics.py
AI/alpha_beta.py
AI/ghost_controller.py
AI/__init__.py
Ghost.py
main.py
```

## Idea De Encierro

Un estado es mejor cuando:

```text
Inky se acerca por una ruta
Clyde cubre otra ruta
PacMan conserva pocas salidas libres
los fantasmas no se amontonan en el mismo pasillo
los fantasmas no repiten ciclos recientes
```

Por eso la evaluacion colaborativa no solo mide distancia.

## Evaluacion Colaborativa

La funcion principal es:

```python
evaluate_pack_state(graph, state)
```

Componentes:

```text
ghost_distances
total_distance_to_pacman
minimum_distance_to_pacman
pacman_escape_routes
covered_exits
free_routes
useful_separation
exit_overlap_penalty
tabu_penalty
```

Interpretacion:

```text
covered_exits alto = mejor
free_routes alto = peor
useful_separation positivo = mejor
exit_overlap_penalty alto = peor
```

## Salidas Cubiertas

Se usa:

```python
pacman_exit_coverage(graph, state)
```

Por cada salida de PacMan, se revisa si Inky o Clyde estan cerca. Si alguno esta dentro de `DEFAULT_PACK_COVERAGE_DISTANCE`, esa salida se considera cubierta.

Esto permite que el algoritmo prefiera:

```text
Inky cubre una salida
Clyde cubre otra salida
```

en lugar de:

```text
Inky y Clyde cubren la misma salida
```

## Alfa-Beta Colaborativo

Se agrego:

```python
choose_pack_action(graph, state, depth=3, tabu_horizon=4)
```

Devuelve:

```python
best_action, best_value, stats
```

Donde:

```text
best_action = (direccion_inky, direccion_clyde)
```

La profundidad recomendada inicial es `3`, porque dos fantasmas generan mas combinaciones que Pinky solo.

## Controlador Compartido

Se agrego:

```python
PackGhostController
```

`main.py` crea una foto antes de actualizar los fantasmas:

```python
pack_controller.set_pack_snapshot(...)
```

Despues:

```text
Inky pide su direccion
Clyde pide su direccion
ambos reciben la misma decision conjunta
```

## Estado Actual En El Juego

```text
ghosts[0] = Blinky rojo aleatorio
ghosts[1] = Pinky rosa alfa-beta
ghosts[2] = Inky azul/cian alfa-beta colaborativo
ghosts[3] = Clyde naranja alfa-beta colaborativo
```

## Pruebas Esperadas

Al probar visualmente, Inky y Clyde no siempre deben seguir el mismo pasillo. Un comportamiento aceptable es que uno se acerque a PacMan mientras el otro queda cerca de una salida alternativa.

Si ambos se amontonan mucho, se deben ajustar:

```text
separation_weight
overlap_weight
covered_exit_weight
free_route_weight
```
