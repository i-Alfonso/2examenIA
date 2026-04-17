# Tema 4: Juegos Con Oponentes

Archivo original:

```text
Tema 4 Juegos_con_Oponentes.pdf
```

## Tema Central

El documento introduce la busqueda con adversarios.

En estos problemas, la secuencia de acciones no depende solo del agente, sino tambien de otro agente que tiene objetivos opuestos.

## Problema General

En un videojuego puede haber varios agentes interactuando.

La pregunta principal es:

```text
Que hacer si un agente debe planear, pero el resultado depende tambien de otro agente?
```

## Juegos Con Dos Agentes

Se describe un escenario con dos agentes:

```text
Agente A
Agente B
```

Ambos interactuan en un tablero dividido en celdas.

El agente A se mueve primero, luego el agente B, y asi sucesivamente.

Objetivos:

```text
A quiere ocupar la misma celda que B
B quiere evitar que A ocupe su celda
```

Esto es directamente comparable con PacMan:

```text
fantasma = perseguidor
PacMan = evasor
```

## Horizonte Limitado

El documento menciona que, por limitaciones de tiempo y computo, no siempre se puede buscar el mejor movimiento exacto.

Por eso se usa analisis con horizonte limitado.

Esto significa buscar solo cierta profundidad y evaluar los nodos finales con una heuristica.

## Minimax

Minimax modela dos jugadores:

```text
MAX = jugador que intenta maximizar la utilidad
MIN = jugador que intenta minimizarla
```

Suposiciones:

- MAX tira primero.
- MIN responde.
- Los niveles pares corresponden a MAX.
- Los niveles impares corresponden a MIN.
- El nodo raiz esta en profundidad cero.

## Funcion De Evaluacion

Los nodos en el limite del horizonte se evaluan con una funcion heuristica.

Ejemplo del documento:

```text
f(tablero) =
  lineas disponibles para MAX
  -
  lineas disponibles para MIN
```

Tambien se pueden usar valores extremos:

```text
infinito positivo si gana MAX
infinito negativo si gana MIN
```

## Etiquetado Minimax

El valor de un nodo depende del tipo de turno:

```text
nodo MAX -> toma maximo de sus hijos
nodo MIN -> toma minimo de sus hijos
```

Tambien se puede usar la convencion:

```text
lo bueno para MAX es malo para MIN
```

## Limitaciones De Minimax

Minimax requiere busqueda exhaustiva dentro del horizonte.

No aplica podas por si mismo.

Esto vuelve costoso el algoritmo cuando el factor de ramificacion aumenta.

## Poda Alfa-Beta

Alfa-beta mejora Minimax manteniendo dos cotas:

```text
alpha = cota inferior
beta = cota superior
```

Si durante la expansion:

```text
alpha >= beta
```

se puede cortar la busqueda de esa rama.

## Algoritmo Alfa-Beta

Idea general:

```text
si nodo es terminal:
    devolver evaluacion heuristica

si nodo es MAX:
    actualizar alpha con el maximo de los hijos
    podar si alpha >= beta

si nodo es MIN:
    actualizar beta con el minimo de los hijos
    podar si alpha >= beta
```

Primer llamado:

```text
alpha = -infinito
beta = infinito
```

## Relacion Con El Proyecto PacMan

Este documento es la base directa de la IA implementada.

En el proyecto:

```text
Pinky = MAX
PacMan = MIN
```

Para Inky y Clyde:

```text
Inky/Clyde como pareja = MAX
PacMan = MIN
```

Se usa horizonte limitado:

```text
Pinky depth = 4
Pack depth = 3
```

Los nodos terminales del horizonte se evaluan con funciones heuristicas:

- Distancia Manhattan entre intersecciones.
- Rutas de escape de PacMan.
- Salidas cubiertas.
- Separacion util entre fantasmas.
- Penalizacion tabu.

La poda alfa-beta se usa para reducir ramas innecesarias.
