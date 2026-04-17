# Busquedas Parte 5: Estrategias Alternativas

Archivo original:

```text
Busquedas Parte 5 Estrategias_Alternativas.pdf
```

## Tema Central

El documento presenta estrategias alternativas y mejoras sobre Minimax y poda alfa-beta para busquedas con oponentes.

La idea principal es que Minimax y alfa-beta son utiles, pero pueden ser costosos cuando el arbol de juego es profundo, denso o cuando el orden de exploracion no favorece las podas.

## Recordatorio Base

En problemas sin adversario se suele usar A* cuando existe una heuristica util.

En juegos con adversario se usan:

- Minimax.
- Poda alfa-beta.

Minimax evalua movimientos propios y respuestas del oponente, pero no poda ramas.

Alfa-beta mejora Minimax usando cotas:

```text
alpha = mejor valor garantizado para MAX
beta = mejor valor garantizado para MIN
```

Cuando `alpha >= beta`, se puede podar la rama.

## Poda De Inutilidades

Es una mejora conceptual sobre alfa-beta.

Mientras alfa-beta poda cuando sabe que una rama no puede mejorar el resultado, la poda de inutilidades poda cuando se estima que una rama no puede mejorar lo suficiente para justificar su expansion.

Requiere definir un umbral de beneficio.

Ese umbral depende del dominio del problema.

## Espera Del Reposo

Tambien aparece como respuesta al efecto horizonte.

El efecto horizonte ocurre cuando una evaluacion en la profundidad limite parece buena o mala, pero si se expandiera un nivel mas, el resultado cambiaria drasticamente.

La espera del reposo continua expandiendo mientras detecte cambios significativos.

Se usa mucho en juegos con intercambio de piezas.

## Busqueda Secundaria

Es una alternativa cuando la espera del reposo puede volverse demasiado costosa.

Primero se usa Minimax o alfa-beta para elegir una rama prometedora.

Luego se hace una segunda busqueda sobre esa rama para verificar que no sea una trampa.

## Extension Singular

Es un caso especial de busqueda secundaria.

Continua expandiendo si existe un movimiento claramente superior a sus hermanos.

La expansion se detiene cuando deja de existir ese movimiento forzado.

El documento menciona el caso de ajedrez y el uso historico en sistemas como Deep Thought.

## Movimientos De Libro

Consisten en usar conocimiento previamente almacenado sobre jugadas conocidas.

Se usan cuando el estado actual coincide con una posicion ya estudiada.

Ejemplos:

- Gato.
- Aperturas de ajedrez.
- Finales de ajedrez.

## Busqueda Sesgada

Reduce o varia el factor de ramificacion.

Las ramas mas prometedoras reciben mas profundidad o mayor expansion.

Tambien se puede usar una estrategia tipo beam search:

```text
solo se expanden los mejores hijos
```

## Minimax Dependiente Del Adversario

Minimax asume que el oponente siempre juega de forma optima.

Eso puede ser demasiado conservador.

Si el adversario comete errores, a veces conviene elegir una rama que no sea la mejor contra un oponente perfecto, pero que tenga mayor oportunidad de castigar errores.

El problema es que requiere modelar probabilidades de error del adversario.

## Bajada Progresiva

Es una tecnica para escenarios con tiempo limitado.

Se realiza busqueda por niveles mientras haya tiempo disponible.

Si el tiempo se agota, se devuelve el mejor camino encontrado hasta ese momento.

## Continuacion Heuristica

Es similar a busqueda secundaria.

Se expande hasta un horizonte inicial y luego se seleccionan ciertos nodos terminales para expandirlos mas.

La seleccion depende del problema.

## Movimiento Nulo

Tecnica para reducir el factor de ramificacion.

La idea general es dar al oponente una jugada de ventaja y verificar si la posicion sigue siendo buena.

Tiene riesgo de perder informacion importante.

## Busqueda Ambiciosa

Tambien llamada aspiration search.

Mejora alfa-beta usando una ventana inicial mas estrecha:

```text
AlfaBeta(nodo, valor - ventana, valor + ventana)
```

En lugar de:

```text
AlfaBeta(nodo, -infinito, infinito)
```

Si la estimacion inicial es buena, puede podar mas.

Si la estimacion es mala, puede requerir repetir la busqueda con una ventana mas amplia.

## NegaMax

Es una simplificacion de Minimax.

Usa la equivalencia:

```text
max(a, b) = -min(-a, -b)
```

Esto permite representar MAX y MIN con una sola forma recursiva.

## NegaScout

Mejora basada en NegaMax.

Asume que el primer hijo explorado es el mejor.

Luego comprueba los demas con una ventana nula.

Si la comprobacion falla, se rehace la busqueda normal para esa rama.

## Profundizacion Iterativa

Incrementa progresivamente la profundidad de busqueda.

Es util cuando hay restricciones de tiempo.

Tambien permite tener siempre una respuesta disponible, aunque el tiempo se agote.

## DFID

Deep First Iterative Deepening combina profundidad limitada con iteraciones crecientes.

Idea:

```text
profundidad = 1
buscar
si no hay solucion, profundidad = 2
buscar
...
```

## IDA*

Iterative Deepening A* combina A* con profundizacion iterativa.

Usa un umbral basado en:

```text
f(n) = g(n) + h(n)
```

Podando ramas que exceden el umbral.

## Relacion Con El Proyecto PacMan

Este documento justifica varias decisiones del proyecto:

- Usar alfa-beta como base.
- Usar profundidad limitada.
- Usar ordenamiento de movimientos para mejorar poda.
- Usar tabu con horizonte limitado como mejora contra ciclos.
- Usar heuristicas para evaluar estados terminales del horizonte.

En el proyecto actual no se implementaron todas estas estrategias alternativas. Las mas relevantes para el examen son:

- Poda alfa-beta.
- Profundidad limitada.
- Ordenamiento de hijos.
- Funcion de evaluacion heuristica.
- Tabu con horizonte limitado.
