# Revision De Cumplimiento Del 2o Parcial

## Objetivo

Este documento resume la revision del proyecto contra el PDF `docs/2o Parcial.pdf` y las notas de clase en `docs/notes`.

La revision se enfoca en:

- cumplimiento de cada inciso del PDF,
- correspondencia con los temas vistos en clase,
- uso de heuristicas,
- mejoras de poda alfa-beta,
- posibles puntos de sobreingenieria,
- documentacion que debe mantenerse al dia.

## Resumen Del Veredicto

El proyecto cumple la parte tecnica central del PDF:

- Blinky rojo se mueve de forma aleatoria.
- Pinky rosa usa poda alfa-beta individual.
- Inky y Clyde usan poda alfa-beta colaborativa.
- Las funciones de evaluacion tienen mas de dos componentes heuristicos.
- Los fantasmas deciden en intersecciones y evitan regresar por donde llegaron si tienen alternativa.
- Alfa-beta incluye busqueda ambiciosa y continuacion heuristica.
- Tabu con horizonte limitado esta integrado.

Los puntos que aun no quedan cubiertos por codigo son entregables externos:

- PDF final de respuestas.
- Video menor a 5 minutos con link accesible.
- Empaquetado final del codigo.

## Inciso 1: Blinky Aleatorio

Estado: cumplido.

El PDF pide:

```text
Blinky rojo con movimiento aleatorio, respetando laberinto, intersecciones y no reversa.
```

En el proyecto:

- `ghosts[0]` usa `fantasma4.bmp`, que corresponde al rojo.
- `tipo=0` hace que use `interseccion_random()`.
- `interseccion_random()` elige una direccion valida segun el codigo de `MC`.
- Se elimina la direccion inversa cuando hay alternativas.
- `can_move_direction()` valida que no salga del tablero ni atraviese pasillos invalidos.

Riesgo menor:

- El movimiento aleatorio no usa semilla fija. Para demostracion esta bien, pero para pruebas reproducibles conviene documentar una secuencia o grabar video claro.

## Inciso 2: Pinky Con Poda Alfa-Beta

Estado: cumplido.

El PDF pide:

```text
Pinky rosa usando poda alfa-beta, funcion de evaluacion con al menos dos componentes heuristicos y reglas de movimiento.
```

En el proyecto:

- `ghosts[1]` usa `fantasma3.bmp`, que corresponde al rosa.
- `PinkyGhostController` construye un `GameState`.
- `choose_pinky_action()` ejecuta alfa-beta.
- La decision se aplica desde `Ghost.path_ia()`.

Funcion de evaluacion:

```text
evaluate_pinky_state()
```

Componentes:

- distancia Manhattan a PacMan,
- rutas de escape de PacMan,
- penalizacion tabu.

Esto supera el minimo de dos componentes heuristicos.

Riesgo menor:

- El documento/reporte final debe explicar por que Manhattan es una heuristica y no pathfinding. Esto es importante porque el profesor ya aclaro que no se debe usar Dijkstra.

## Inciso 3: Inky Y Clyde Cooperativos

Estado: cumplido.

El PDF pide:

```text
Dos fantasmas, Inky/Clyde, con movimiento colaborativo para cazar en manada usando alfa-beta.
```

En el proyecto:

- `ghosts[2]` usa `fantasma2.bmp`, azul/cian.
- `ghosts[3]` usa `fantasma1.bmp`, naranja.
- Ambos comparten `PackGhostController`.
- `set_pack_snapshot()` congela la posicion de ambos antes de decidir.
- `choose_pack_action()` devuelve una accion conjunta:

```text
(direccion_inky, direccion_clyde)
```

Funcion de evaluacion:

```text
evaluate_pack_state()
```

Componentes:

- distancia total a PacMan,
- distancia minima a PacMan,
- rutas de escape de PacMan,
- salidas cubiertas,
- rutas libres,
- separacion util,
- penalizacion por cubrir la misma salida,
- penalizacion tabu.

Esto cumple la idea de caza en manada porque no solo premia acercarse; tambien premia cerrar rutas.

Riesgo menor:

- La colaboracion se decide en una accion conjunta, lo cual es correcto, pero el comportamiento visual puede depender mucho de los pesos. En el video conviene mostrar casos donde uno persigue y el otro bloquea.

## Inciso 4: Alfa-Beta, Mejoras Y Tabu

Estado: cumplido con observaciones.

El PDF pide:

```text
Implementar poda alfa-beta aplicable a las preguntas previas, con dos estrategias de mejora vistas en clase, incluyendo por default Tabu con horizonte limitado.
```

Base implementada:

- `alpha_beta()`
- `choose_best_action()`
- `choose_pinky_action()`
- `choose_pack_action()`

Mejoras principales implementadas:

```text
1. Busqueda ambiciosa
2. Continuacion heuristica
```

Ambas aparecen en las notas de `Busquedas Parte 5 Estrategias_Alternativas.md`.

Tabu:

- `GameState.tabu` guarda memoria limitada.
- `with_tabu_item()` conserva solo los ultimos elementos.
- `tabu_horizon=4` se usa por defecto.
- La evaluacion penaliza estados tabu.

Observacion importante:

El tabu esta implementado como penalizacion, no como prohibicion absoluta. Esto es defendible porque evita bloquear fantasmas en pasillos con pocas opciones, pero en el reporte conviene decirlo de forma explicita.

## Inciso 5: Video Y Entregables

Estado: pendiente.

El codigo no puede cubrir por si solo:

- video,
- link accesible,
- PDF final,
- archivo comprimido final.

Accion necesaria:

- preparar reporte con pseudocodigo, heuristicas y evidencia,
- grabar video menor a 5 minutos,
- verificar permisos del link,
- comprimir codigo final.

## Relacion Con Notas De Clase

Notas usadas directamente:

```text
Tema 4 Juegos_con_Oponentes.md
Busquedas Parte 5 Estrategias_Alternativas.md
Tema 3 Agentes Busquedas 2026-1.md
```

Conceptos aplicados:

- estados,
- acciones,
- modelo de transicion,
- funcion de evaluacion,
- heuristicas,
- minimax,
- poda alfa-beta,
- horizonte limitado,
- busqueda ambiciosa,
- continuacion heuristica,
- tabu con horizonte limitado.

Conceptos no usados:

- Dijkstra,
- A*,
- IDA*,
- algoritmos geneticos,
- recocido simulado,
- busqueda de camino minimo,
- NegaMax,
- NegaScout,
- movimiento nulo,
- movimientos de libro.

Esto es bueno porque evita alejarse del enunciado.

## Posible Sobreingenieria

El proyecto tiene mas estructura que el codigo base original, pero la mayor parte esta justificada:

```text
MazeControl
  justificado: encapsula consultas a MC sin usar Dijkstra.

GameState
  justificado: alfa-beta necesita estados inmutables para simular ramas.

alpha_beta
  justificado: requisito central del PDF.

heuristics
  justificado: requisito central del PDF.

ghost_controller
  justificado: separa IA del dibujo y movimiento visual.
```

Partes que pueden sentirse extra:

- metricas de busqueda,
- logs de captura,
- transparencia de sprites,
- camara cenital,
- buffer de direccion de PacMan.

Estas partes no son requisitos de IA. Se deben presentar como soporte para pruebas o jugabilidad, no como parte principal del algoritmo.

## Recomendacion Para Defender El Proyecto

En reporte y exposicion conviene centrar la explicacion en:

1. `MC`, `xMC`, `yMC` como base de intersecciones.
2. `MazeControl` como adaptador simple sobre esa matriz.
3. `GameState` como estado para alfa-beta.
4. Blinky aleatorio.
5. Pinky con alfa-beta individual.
6. Inky/Clyde con accion conjunta.
7. Heuristicas.
8. Busqueda ambiciosa.
9. Continuacion heuristica.
10. Tabu con horizonte limitado.

Evitar venderlo como pathfinding.

Frase recomendada:

```text
No usamos Dijkstra ni camino minimo. La busqueda adversarial decide entre movimientos legales de interseccion y las heuristicas usan Manhattan como estimacion.
```

## Veredicto

Como entrega de codigo, el proyecto esta tecnicamente alineado con el PDF.

Como entrega completa del parcial, todavia faltan los entregables externos:

- PDF final,
- video,
- link verificable,
- comprimido final.

El riesgo principal no es tecnico, sino de argumentacion: el reporte debe dejar claro que la matriz de control solo genera movimientos legales y que la decision real la toma alfa-beta con heuristicas vistas en clase.
