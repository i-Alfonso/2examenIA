# Maze Control

## Objetivo

Se agrego `IA/maze_control.py` para consultar directamente la matriz de control `MC`.

La idea es mantener el proyecto simple:

```text
MC, xMC, yMC -> MazeControl -> movimientos legales para alfa-beta
```

No se construye una matriz de adyacencia aparte ni una busqueda de camino minimo. `MazeControl` solo responde preguntas necesarias para simular movimientos en intersecciones.

## Por Que Se Cambio

Antes existia una clase enfocada en representar el laberinto como estructura de busqueda. Funcionaba, pero podia hacer parecer que el proyecto dependia de algo mas complejo de lo necesario.

El PDF no pide implementar una matriz de control. Pide que los fantasmas:

- cambien direccion solo en intersecciones,
- no regresen por donde llegaron si tienen alternativas,
- usen poda alfa-beta,
- usen funciones de evaluacion con heuristicas,
- incluyan dos mejoras vistas en clase,
- usen tabu con horizonte limitado.

Por eso ahora se trabaja directamente con `MC`.

## Datos Que Usa

```text
MC
  matriz compacta de intersecciones.

xMC
  coordenadas X reales de las columnas de MC.

yMC
  coordenadas Z/Y reales de las filas de MC.
```

Cada celda distinta de cero en `MC` es una interseccion o punto de control.

## Direcciones

Se conservan los codigos originales del proyecto:

```text
0 = arriba
1 = derecha
2 = abajo
3 = izquierda
```

## Tipos De Interseccion

`MazeControl.ALLOWED_DIRECTIONS` define que direcciones permite cada codigo de `MC`.

Ejemplo:

```text
10 -> derecha, abajo
25 -> arriba, derecha, abajo, izquierda
26 -> derecha
27 -> izquierda
```

Esto evita calcular movimientos por pixel dentro de alfa-beta.

## Clase Principal

```python
from IA import MazeControl

maze_control = MazeControl(MC, xMC, yMC)
```

## Funciones Principales

### get_neighbors(node)

Devuelve las opciones legales desde una interseccion.

```python
maze_control.get_neighbors((0, 0))
```

Cada opcion contiene:

```text
target
direction
cost
```

### next_node(node, direction)

Devuelve la opcion que se alcanza si desde `node` se toma `direction`.

```python
maze_control.next_node((0, 0), 1)
```

### node_to_pixel(node)

Convierte una interseccion de `MC` a coordenadas del juego.

```python
maze_control.node_to_pixel((0, 0))
```

Resultado esperado:

```python
(20, 20)
```

### pixel_to_node(x, z)

Convierte una posicion del juego a interseccion de `MC`.

```python
maze_control.pixel_to_node(20, 20)
```

Resultado esperado:

```python
(0, 0)
```

## Distancias

No se usa busqueda de camino minimo.

Las heuristicas usan distancia Manhattan entre coordenadas de intersecciones:

```text
abs(x1 - x2) + abs(y1 - y2)
```

Esto mantiene la decision dentro de alfa-beta.

## Relacion Con Alfa-Beta

`MazeControl` solo da movimientos posibles.

La decision sigue este flujo:

```text
fantasma llega a interseccion
MazeControl obtiene opciones legales desde MC
GameState genera hijos
alfa-beta simula turnos MAX/MIN
la funcion de evaluacion asigna score
el controlador devuelve una direccion
```

## Validaciones

Con los datos actuales del proyecto:

```text
66 intersecciones
170 conexiones dirigidas calculadas desde MC
0 conexiones asimetricas
```

Estas validaciones solo comprueban que `MC`, `xMC` y `yMC` son consistentes.
