# Tema 3: Agentes Que Resuelven Problemas y Busquedas

Archivo original:

```text
Tema 3 Agentes Busquedas 2026-1.pdf
```

## Tema Central

El documento introduce la formulacion de problemas de busqueda y los algoritmos principales para resolverlos.

La idea base es que muchos problemas de inteligencia artificial se pueden modelar como:

```text
estado inicial
acciones posibles
modelo de transicion
prueba de meta
costo del camino
```

## Busqueda

Busqueda es el procedimiento de exploracion usado para decidir una accion o una secuencia de acciones.

Se usa cuando un agente necesita encontrar una ruta desde un estado inicial hasta una meta.

## Formulacion De Problemas

Para formular un problema se debe decidir:

- Que estados existen.
- Que acciones se pueden ejecutar.
- Como se detecta la meta.
- Que costo tiene cada camino.
- Como se puede guiar la busqueda.

Ejemplo usado:

```text
8-puzzle
```

Preguntas importantes:

- Cuales son los estados.
- Cuales son las acciones.
- Cual es la prueba de meta.
- Cual es el costo del camino.

## Costo Total

El documento separa:

```text
Costo total = costo de busqueda + costo del camino
```

Esto es importante porque una solucion barata en camino puede ser muy cara de encontrar, o una busqueda barata puede encontrar un camino peor.

## Busqueda En Arboles

Se parte de un estado inicial y se expanden estados vecinos.

Proceso general:

```text
crear arbol con estado inicial
mientras existan candidatos:
    elegir nodo segun estrategia
    si es meta, regresar solucion
    si no, expandir sucesores
si no quedan candidatos, fallar
```

## Busqueda Primero En Anchura

Tambien conocida como breadth-first search.

Expande primero el nodo raiz, luego todos sus sucesores, luego los sucesores de esos sucesores.

Usa estructura FIFO.

Propiedades:

- Completa en espacios finitos.
- Tiempo aproximado: `O(b^d)`.
- Espacio aproximado: `O(b^d)`.

Variables:

```text
b = factor de ramificacion
d = profundidad de la solucion
```

## Busqueda Primero En Profundidad

Tambien conocida como depth-first search.

Expande el nodo no expandido mas profundo.

Usa estructura LIFO.

Propiedades:

- Completa en espacios finitos.
- Tiempo aproximado: `O(b^d)`.
- Espacio aproximado: `O(bm)`.

Variables:

```text
m = profundidad maxima de expansion
```

## Consideraciones Sobre Busqueda

El factor de ramificacion de un estado indica cuantos sucesores puede tener.

Un algoritmo es completo si encuentra solucion siempre que el problema sea soluble.

Busqueda en profundidad suele ser preferible cuando las soluciones estan alejadas.

Busqueda en anchura suele ser preferible cuando las soluciones estan cerca.

## Profundizacion Iterativa

Controla la expansion aumentando gradualmente la profundidad.

Ejemplo:

```text
buscar a profundidad 1
si falla, buscar a profundidad 2
si falla, buscar a profundidad 3
...
```

Combina ventajas de busqueda en profundidad y busqueda por niveles.

## Busqueda Local

Se usa cuando el espacio de busqueda es muy grande.

No intenta explorar todo el camino global desde inicio hasta meta.

Busca mejorar soluciones locales.

Caracteristicas:

- Usa poca memoria.
- No necesariamente es completa.
- Puede encontrar soluciones razonables en problemas grandes.

Proceso general:

```text
iniciar con una solucion posible
evaluar vecinos
moverse al mejor vecino
repetir hasta no mejorar
```

## Busqueda Local: Algoritmos

El documento menciona:

- Hill climbing.
- Recocido simulado.
- Busqueda tabu.
- Algoritmos evolutivos o geneticos.

## Busqueda Global

Explora todo o gran parte del espacio de busqueda para buscar la mejor solucion.

Se usa cuando:

- Hay muchos maximos o minimos locales.
- Se requiere una solucion optima o muy cercana.

Algoritmos mencionados:

- Recocido simulado.
- Algoritmos geneticos.
- Busqueda aleatoria global.
- Enjambre de particulas.
- Colonias de hormigas.

## Heuristica

Una heuristica es una funcion de evaluacion basada en conocimiento del problema.

Sirve para identificar estados prometedores.

Puede sacrificar optimalidad o completez a cambio de eficiencia.

Funciones comunes:

```text
f(n) = g(n)
f(n) = h(n)
f(n) = g(n) + h(n)
```

Donde:

```text
g(n) = costo desde estado inicial hasta n
h(n) = costo estimado desde n hasta la meta
```

## Hill Climbing

Selecciona un nodo actual y se mueve al vecino con mejor evaluacion.

No guarda informacion para volver atras.

Puede atascarse en:

- Optimos locales.
- Mesetas.
- Crestas.

Variantes:

- Simple hill climbing.
- Steepest ascent hill climbing.
- Random restart hill climbing.
- Stochastic hill climbing.

## Recocido Simulado

Algoritmo inspirado en el enfriamiento de metales.

Permite aceptar soluciones peores con cierta probabilidad para escapar de optimos locales.

La probabilidad depende de la temperatura.

Ventajas:

- Escapa de optimos locales.
- Es flexible.
- Funciona en problemas grandes.

Desventajas:

- Depende mucho de parametros.
- Puede ser lento.
- No garantiza optimo global.

## Busqueda Tabu

Busqueda local avanzada con memoria.

Evita ciclos y soluciones ya visitadas mediante una lista tabu.

La lista puede almacenar:

- Movimientos.
- Soluciones.
- Caracteristicas de soluciones.

El contenido se considera prohibido durante un numero limitado de iteraciones.

Ventajas:

- Evita ciclos.
- Escapa de optimos locales.
- Es adaptable.

Desventajas:

- Requiere disenar bien la lista tabu.
- Depende de parametros.
- No garantiza optimo global.

## Best First Search

Selecciona siempre el nodo mas prometedor segun una funcion de evaluacion.

Ventaja:

- Puede llegar a una solucion sin expandir todo el arbol.

Desventaja:

- El camino no necesariamente es optimo.

Funciones posibles:

```text
f(n) = g(n)
f(n) = h(n)
```

## A*

A* combina costo real y estimacion heuristica:

```text
f(n) = g(n) + h(n)
```

El documento usa un ejemplo con 8-puzzle.

## Relacion Con El Proyecto PacMan

Este tema fundamenta el modelado del laberinto como problema de busqueda.

En el proyecto:

- Los estados son posiciones en intersecciones.
- Las acciones son direcciones posibles.
- La meta es alcanzar o encerrar a PacMan.
- El costo de cada tramo se mide entre intersecciones vecinas de `MC`.
- Las heuristicas guian alfa-beta.
- Tabu evita ciclos recientes.

Tambien justifica usar distancia Manhattan como heuristica, sin convertir el problema en camino minimo.
