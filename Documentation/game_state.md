# Game State

## Objetivo

Se agrego `AI/game_state.py` para representar los estados que usara alfa-beta.

El grafo (`MazeGraph`) sabe como esta conectado el laberinto. Pero alfa-beta necesita algo mas: necesita saber donde estan PacMan y los fantasmas en un momento especifico.

Ese "momento especifico" es un estado del juego.

## Archivos Agregados

```text
AI/game_state.py
```

Tambien se actualizo:

```text
AI/__init__.py
```

para poder importar las clases y funciones nuevas desde el paquete `AI`.

## ActorState

`ActorState` representa a un personaje dentro del grafo.

Puede representar:

- PacMan.
- Pinky.
- Inky.
- Clyde.

Estructura:

```python
ActorState(
    node=(0, 0),
    direction=1,
)
```

Campos:

```text
node
  interseccion donde esta el actor.

direction
  direccion actual del actor.
```

Direcciones:

```text
0 = arriba
1 = derecha
2 = abajo
3 = izquierda
```

## GameState

`GameState` representa el estado completo usado por la busqueda.

Estructura:

```python
GameState(
    pacman=ActorState(node=(0, 0), direction=1),
    ghosts=(
        ActorState(node=(9, 9), direction=3),
    ),
    turn="ghosts",
    tabu=(),
)
```

Campos:

```text
pacman
  estado de PacMan.

ghosts
  tupla con uno o mas fantasmas.

turn
  indica quien mueve en ese nivel de busqueda.

tabu
  historial de estados o nodos recientes para evitar ciclos.
```

Para Pinky, `ghosts` tendra un fantasma.

Para Inky y Clyde, `ghosts` tendra dos fantasmas.

## Por Que Usar Estados Inmutables

Las clases usan:

```python
@dataclass(frozen=True)
```

Esto significa que el estado no se modifica directamente. En vez de cambiar el objeto actual, se crea otro estado nuevo.

Esto es importante para alfa-beta porque la busqueda simula muchos futuros posibles.

Si se modificara el mismo objeto en cada rama, una rama podria contaminar a otra.

## Funciones Principales

### actor_from_position

Convierte una posicion real del juego a un `ActorState`.

Ejemplo:

```python
actor_from_position(graph, [20, 1, 20], direction=1)
```

Resultado:

```python
ActorState(node=(0, 0), direction=1)
```

Esto sirve para conectar el juego visual con el modelo de busqueda.

### legal_edges

Devuelve los movimientos legales de un actor.

Para fantasmas, normalmente se usa:

```python
legal_edges(graph, ghost, avoid_reverse=True)
```

Eso aplica la regla:

```text
el fantasma no puede regresarse por el camino por donde llego
```

Si no hay otra opcion, se permite regresar para no bloquear al actor.

### legal_directions

Devuelve solo las direcciones legales.

Ejemplo:

```python
legal_directions(graph, actor)
```

Resultado posible:

```python
(1, 2)
```

Eso significa:

```text
derecha y abajo
```

### generate_pacman_children

Genera estados hijos cuando PacMan mueve.

PacMan no usa la regla de no regresar porque el jugador si puede invertir direccion.

Se usara cuando alfa-beta modele a PacMan como el jugador minimizador.

### generate_single_ghost_children

Genera estados hijos para un solo fantasma.

Esto se usara para Pinky.

Ejemplo conceptual:

```text
Pinky esta en una interseccion.
Tiene 3 movimientos posibles.
Se generan 3 estados hijos.
```

### generate_joint_ghost_children

Genera estados hijos para dos fantasmas que deciden en conjunto.

Esto se usara para Inky y Clyde.

Ejemplo conceptual:

```text
Inky tiene 2 movimientos posibles.
Clyde tiene 3 movimientos posibles.
Se generan 2 x 3 = 6 estados hijos conjuntos.
```

Esto permite modelar la caza colaborativa.

## Relacion Con Alfa-Beta

Alfa-beta necesitara tres piezas:

```text
estado actual
generador de hijos
funcion de evaluacion
```

Con `game_state.py`, ya se tiene:

```text
estado actual
generador inicial de hijos
```

Todavia falta:

```text
AI/alpha_beta.py
AI/heuristics.py
AI/tabu.py
AI/ghost_controller.py
```

## Lo Que Sigue

El siguiente paso recomendado es implementar:

```text
AI/heuristics.py
```

Primero para Pinky:

```text
distancia real entre Pinky y PacMan
penalizacion por ciclos
bonus por acercarse
```

Despues:

```text
AI/alpha_beta.py
```

para elegir la mejor accion usando esos estados hijos.
