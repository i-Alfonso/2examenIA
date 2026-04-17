# Mejoras De Busqueda

## Objetivo

Este documento resume las mejoras de busqueda agregadas sobre poda alfa-beta para cumplir el inciso 4 del parcial.

El enunciado pide:

```text
Implementar el algoritmo poda alfa-beta...
incluyendo dos estrategias de mejora platicadas en clase
(continuacion heuristica, busqueda ambiciosa, etc.),
incluyendo por default Tabu con horizonte limitado.
```

## Mejoras Principales

Las dos mejoras principales implementadas son:

```text
1. Busqueda ambiciosa
2. Continuacion heuristica
```

Ademas se mantiene:

```text
Tabu con horizonte limitado
```

## Busqueda Ambiciosa

La busqueda ambiciosa usa una ventana alfa-beta inicial mas estrecha.

En lugar de iniciar siempre con:

```python
alpha = -inf
beta = inf
```

se intenta:

```python
alpha = expected_value - aspiration_window
beta = expected_value + aspiration_window
```

Si el resultado queda dentro de la ventana, se acepta.

Si queda fuera, se repite con ventana completa.

En el proyecto:

```text
expected_value = ultimo valor alfa-beta del controlador
```

Valores actuales:

```text
Pinky aspiration_window = 80
Pack aspiration_window = 120
```

## Continuacion Heuristica

La continuacion heuristica reduce el efecto horizonte.

Cuando se llega a la profundidad limite, se revisa si el estado es critico.

Si es critico, se expande un nivel adicional:

```text
heuristic_continuation_depth = 1
```

Para Pinky se considera critico si:

```text
distancia a PacMan <= 120
PacMan tiene 3 o mas rutas de escape
```

Para Inky/Clyde se considera critico si:

```text
distancia minima a PacMan <= 120
PacMan tiene rutas libres
Inky y Clyde cubren la misma salida
```

## Tabu Con Horizonte Limitado

El tabu se guarda dentro de:

```text
GameState.tabu
```

Cada movimiento simulado de fantasma agrega el nodo nuevo al historial.

El historial conserva solo los ultimos elementos:

```text
tabu_horizon = 4
```

El tabu se aplica como penalizacion, no como prohibicion absoluta.

## Optimizaciones Complementarias

Tambien se mantienen:

```text
ordenamiento de movimientos
corte por captura
metricas de busqueda
```

Las metricas nuevas son:

```text
aspiration_searches
aspiration_researches
heuristic_continuations
```

## Archivos Relacionados

```text
IA/alpha_beta.py
IA/ghost_controller.py
IA/game_state.py
IA/heuristics.py
```
