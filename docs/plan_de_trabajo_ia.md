# Plan De Trabajo Para Completar La IA Del PacMan

## Objetivo Del Proyecto

El objetivo del examen no es rehacer todo PacMan desde cero. El proyecto base ya dibuja el tablero, carga texturas, mueve a PacMan y mueve fantasmas de forma aleatoria.

Lo que faltaba era implementar la toma de decisiones de los fantasmas usando poda alfa-beta, funciones de evaluacion, heuristicas y movimiento colaborativo.

Estado actual: Blinky ya queda como fantasma aleatorio, Pinky usa alfa-beta individual, e Inky/Clyde usan alfa-beta colaborativo.

La estrategia recomendada es conservar el proyecto base lo mas intacto posible y agregar la nueva logica de IA en archivos nuevos. El codigo existente solo debe llamar esas funciones cuando un fantasma necesite decidir hacia donde moverse.

## Estado Actual Del Proyecto

### Lo Que Ya Funciona

- El tablero se renderiza con `pygame` y `OpenGL`.
- El mapa se carga desde `mapa.csv`.
- Las texturas se cargan desde archivos `.bmp`.
- PacMan se mueve manualmente con `W`, `A`, `S`, `D`.
- La camara rota con flecha izquierda y flecha derecha.
- La camara sube y baja con flecha arriba y flecha abajo.
- Los fantasmas se dibujan sobre el tablero.
- Los fantasmas pueden moverse aleatoriamente por el laberinto.
- Los fantasmas respetan la regla de cambiar direccion solo en intersecciones.
- Los fantasmas evitan regresar inmediatamente por el camino por donde llegaron.
- Existe una matriz de control `MC` que representa las intersecciones importantes.
- Existen arreglos `xMC` y `yMC` que conectan la matriz `MC` con coordenadas reales del mapa.
- `mapa.csv`, `mapa_codigos.csv` y `MC` ya contienen la informacion base para tomar decisiones solo en intersecciones.
- La idea del proyecto base es que los personajes avancen por pixeles, pero que las decisiones relevantes se tomen unicamente al llegar a una interseccion.

### Lo Que Todavia Falta

- Probar visualmente los cuatro fantasmas dentro del juego.
- Ajustar pesos de la heuristica colaborativa si Inky/Clyde se amontonan o no bloquean salidas.
- Revisar logs de rendimiento y ajustar comportamiento.
- Preparar reporte final en PDF.
- Preparar guion o estructura del video.

### Lo Que Ya Se Agrego En El Modulo AI

- `AI/maze_graph.py`: estructura de grafo derivada de las intersecciones existentes.
- `AI/game_state.py`: estado de busqueda y generacion inicial de hijos.
- `AI/heuristics.py`: evaluacion para Pinky y evaluacion colaborativa para Inky/Clyde.
- `AI/alpha_beta.py`: poda alfa-beta reutilizable, Pinky y acciones conjuntas.
- `AI/ghost_controller.py`: puente entre el juego visual y la IA.
- `Ghost.py`: validacion de bordes para impedir que los fantasmas salgan del tablero.

## Requisitos Del PDF Del Examen

### Inciso 1: Blinky Aleatorio

Se pide un fantasma rojo con movimiento aleatorio.

Debe cumplir:

- Moverse por el laberinto.
- Cambiar direccion solo en intersecciones.
- No regresarse por el camino por donde llego.

Estado actual:

- Este punto esta resuelto en `Ghost.py` y `main.py`.
- La funcion `interseccion_random()` ya selecciona movimientos aleatorios validos.
- El fantasma rojo usa `fantasma4.bmp` y queda configurado como Blinky.

Acciones pendientes de reporte:

- Agregar explicacion en el reporte.
- Opcionalmente agregar semilla fija para pruebas reproducibles.

### Inciso 2: Pinky Con Poda Alfa-Beta

Se pide un fantasma rosa que use poda alfa-beta para alcanzar a PacMan.

Debe cumplir:

- Usar una funcion de evaluacion.
- Incluir al menos dos componentes heuristicas.
- Respetar reglas de movimiento del laberinto.
- Argumentar el diseno de la funcion.

Estado actual:

- Implementado.
- Pinky usa `PinkyGhostController`.
- La funcion `path_ia()` llama al controlador cuando `tipo=1`.
- `ghosts[1]` se inicializa como Pinky rosa con alfa-beta.

Acciones pendientes de ajuste:

- Probar visualmente.
- Ajustar profundidad si el juego se vuelve lento.
- Documentar resultados.

Heuristicas recomendadas para Pinky:

- Distancia por pasos sobre el grafo entre Pinky y PacMan.
- Penalizacion si Pinky se aleja del PacMan respecto al estado anterior.
- Penalizacion tabu para evitar ciclos.
- Bonus si Pinky queda en una interseccion con varias salidas hacia PacMan.

La distancia debe ser sobre el grafo del laberinto, no distancia euclidiana directa. Esto es importante porque en un laberinto una distancia visual corta puede estar bloqueada por paredes.

### Inciso 3: Inky Y Clyde Colaborativos

Se piden dos fantasmas con movimiento colaborativo tipo "cazar en manada".

Debe cumplir:

- Usar poda alfa-beta.
- Usar una funcion de evaluacion.
- Incluir al menos dos componentes heuristicas.
- Respetar reglas de movimiento.
- Argumentar el diseno.

Estado actual:

- Implementado en primera version.
- Inky y Clyde usan `PackGhostController`.
- La accion colaborativa se calcula como `(direccion_inky, direccion_clyde)`.
- Clyde se movio a otra posicion inicial para no empezar encima de Inky.

Acciones pendientes de ajuste:

- Probar visualmente que no se amontonen.
- Ajustar pesos de cobertura, rutas libres, separacion y solapamiento.
- Revisar las metricas/logs para explicar el comportamiento.

Heuristicas recomendadas para colaboracion:

- Distancia minima de cualquier fantasma a PacMan.
- Suma de distancias de ambos fantasmas a PacMan.
- Cobertura de salidas de PacMan.
- Penalizacion si los dos fantasmas estan demasiado juntos.
- Bonus si los fantasmas atacan desde direcciones distintas.
- Penalizacion tabu para evitar ciclos repetitivos.

La idea no debe ser solo que ambos corran hacia PacMan. Para que parezca "caza en manada", uno puede acercarse directamente y el otro puede bloquear rutas de escape.

### Inciso 4: Poda Alfa-Beta Reutilizable

Se pide implementar poda alfa-beta de forma aplicable a los incisos anteriores.

Debe incluir:

- Pseudocodigo.
- Implementacion.
- Dos estrategias de mejora vistas en clase.
- Tabu con horizonte limitado por default.

Estado actual:

- No existe.

Acciones pendientes:

- Crear archivo nuevo para alfa-beta.
- Hacer que el algoritmo reciba funciones externas:
  - generador de hijos,
  - evaluador,
  - prueba de terminal,
  - profundidad maxima.
- Agregar ordenamiento de movimientos como mejora.
- Agregar continuacion heuristica o busqueda ambiciosa como mejora.
- Agregar tabu con horizonte limitado.

Estrategias recomendadas:

- Ordenamiento de movimientos: evaluar primero los movimientos que parecen acercarse mas a PacMan.
- Busqueda ambiciosa: priorizar caminos con mejor evaluacion heuristica inmediata.
- Tabu con horizonte limitado: recordar ultimos nodos o estados para evitar ciclos.

Punto importante:

El PDF dice "incluyendo dos estrategias de mejora" e "incluyendo por default Tabu con horizonte limitado". Conviene implementar tabu y ademas otra mejora clara, para evitar una interpretacion estricta del profesor.

### Inciso 5: Video Y Entregables

Se pide:

- PDF con respuestas.
- Codigo comprimido.
- Video de maximo 5 minutos.

Estado actual:

- No existe PDF final.
- No existe video.
- Ya existen notas utiles para preparar el reporte.

Acciones pendientes:

- Documentar la arquitectura.
- Documentar alfa-beta.
- Documentar las heuristicas.
- Grabar ejecucion mostrando:
  - Blinky aleatorio,
  - Pinky persiguiendo,
  - Inky/Clyde colaborando,
  - controles basicos.

## Diseno Modular Recomendado

Para evitar modificar demasiado el proyecto base, se recomienda crear una carpeta nueva:

```text
AI/
```

Contenido recomendado:

```text
AI/
  __init__.py
  maze_graph.py
  game_state.py
  alpha_beta.py
  heuristics.py
  tabu.py
  ghost_controller.py
```

### AI/maze_graph.py

Responsabilidad:

- Convertir las intersecciones existentes en `MC`, `xMC`, `yMC` y/o `mapa_codigos.csv` en una estructura de grafo.
- Mantener la misma idea del proyecto base: tomar decisiones solo en intersecciones, no en cada pixel.
- Guardar nodos.
- Guardar aristas.
- Guardar costos entre nodos.
- Traducir direccion a siguiente nodo.
- Traducir posicion de pixel a nodo cercano.

Funciones sugeridas:

```python
build_graph(mc, x_coords, y_coords)
get_neighbors(node)
get_cost(origin, destination)
direction_between(origin, destination)
pixel_to_node(x, z)
node_to_pixel(node)
```

### AI/game_state.py

Responsabilidad:

- Representar el estado usado por alfa-beta.

Datos sugeridos:

```python
pacman_node
pacman_direction
ghost_nodes
ghost_directions
turn
tabu_history
depth
```

Para Pinky, `ghost_nodes` puede tener un solo fantasma.

Para Inky/Clyde, `ghost_nodes` debe tener dos fantasmas.

### AI/alpha_beta.py

Responsabilidad:

- Implementar poda alfa-beta generica.

Debe evitar depender de `pygame`, `OpenGL`, `Pacman.py` o `Ghost.py`.

Firma sugerida:

```python
alpha_beta(state, depth, alpha, beta, maximizing, generate_children, evaluate)
```

Tambien se puede crear una funcion auxiliar:

```python
choose_best_action(state, depth, generate_children, evaluate)
```

### AI/heuristics.py

Responsabilidad:

- Contener funciones de evaluacion.
- La primera version ya incluye la evaluacion individual de Pinky.

Funciones actuales:

```python
graph_distance(graph, origin, destination)
distance_to_pacman(graph, state)
pacman_escape_routes(graph, state)
pinky_heuristic_components(graph, state)
evaluate_pinky_state(graph, state)
```

Funciones agregadas para la parte colaborativa:

```python
evaluate_pack_state(graph, state)
pack_heuristic_components(graph, state)
pacman_exit_coverage(graph, state)
useful_separation_score(graph, state)
exit_overlap_penalty(graph, state)
```

### Tabu Con Horizonte Limitado

Responsabilidad:

- Manejar historial tabu para penalizar ciclos recientes.
- Mantener una memoria corta dentro de cada `GameState`.
- Evitar que el fantasma repita nodos recientes sin prohibir movimientos legales.

Estado actual:

```text
El tabu ya esta integrado en GameState, alpha_beta y heuristics.
No se creo AI/tabu.py porque todavia no hace falta separar esa logica.
```

### AI/ghost_controller.py

Responsabilidad:

- Ser el puente entre los fantasmas existentes y el modulo de IA.
- Recibir posiciones actuales.
- Convertir posiciones a nodos.
- Ejecutar alfa-beta.
- Devolver una direccion `0`, `1`, `2` o `3`.

Direcciones usadas por el proyecto:

```text
0 = arriba
1 = derecha
2 = abajo
3 = izquierda
```

## Cambios Minimos En El Codigo Existente

### main.py

Cambios esperados:

- Importar los controladores de IA.
- Crear el grafo una sola vez.
- Crear controladores para Pinky, Inky y Clyde.
- Pasar referencias a los fantasmas.

Ejemplo conceptual:

```python
from AI.maze_graph import MazeGraph
from AI.ghost_controller import GhostController

maze_graph = MazeGraph(MC, xMC, yMC)
pinky_controller = GhostController(maze_graph, mode="pinky")
pack_controller = GhostController(maze_graph, mode="pack")
```

### Ghost.py

Cambios esperados:

- Agregar soporte para recibir un controlador.
- Si el fantasma es aleatorio, seguir usando `interseccion_random()`.
- Si el fantasma usa IA, pedir direccion al controlador.

Ejemplo conceptual:

```python
if self.tipo == 0:
    self.interseccion_random()
else:
    self.direction = self.controller.next_direction(...)
```

### Pacman.py

Cambios esperados:

- Idealmente ninguno al inicio.
- Mas adelante podria exponer una funcion para consultar direccion y nodo actual.

## Orden De Implementacion Recomendado

### Paso 1: Crear El Modulo AI

Crear:

```text
AI/__init__.py
AI/maze_graph.py
```

Objetivo:

- Construir una representacion formal del grafo a partir de las intersecciones que ya existen.
- Usar `MC`, `xMC`, `yMC` y, si conviene, validar contra `mapa_codigos.csv`.
- Evitar que alfa-beta tome decisiones por pixel.
- Confirmar que hay 66 nodos.
- Confirmar que el grafo esta conectado.
- Confirmar que todas las aristas son reciprocas.

Criterio de exito:

- Un script de prueba imprime los nodos y vecinos sin abrir la ventana OpenGL.

### Paso 2: Crear Pruebas Basicas Del Grafo

Crear una prueba o script simple que valide:

- Cantidad de nodos.
- Cantidad de aristas.
- Conectividad.
- Conversion pixel a nodo.
- Conversion nodo a pixel.

Criterio de exito:

- PacMan inicial `(20, 20)` corresponde al nodo `(0, 0)`.
- Fantasma inferior derecho `(378, 380)` corresponde al nodo `(9, 9)`.

### Paso 3: Implementar Distancias En El Grafo

Agregar distancia minima usando BFS o Dijkstra.

Como las aristas tienen costos distintos en pixeles, Dijkstra es mejor que BFS.

Criterio de exito:

- Se puede calcular distancia de cualquier nodo a cualquier otro.
- La distancia respeta paredes porque viaja por el grafo, no por linea recta.

### Paso 4: Crear GameState

Crear una representacion simple del estado.

Para Pinky:

```text
PacMan node
Pinky node
PacMan direction
Pinky direction
turn
tabu
```

Para Inky/Clyde:

```text
PacMan node
Inky node
Clyde node
directions
turn
tabu
```

Criterio de exito:

- Se pueden crear estados sin depender de OpenGL.

### Paso 5: Generar Hijos

Implementar acciones legales.

Reglas:

- En una interseccion, puede elegir direcciones permitidas por el nodo.
- No debe regresar por la direccion inversa, excepto si no hay otra opcion o si se decide permitirlo para PacMan.
- El resultado de una accion debe ser el siguiente nodo alcanzado.

Criterio de exito:

- Desde cada nodo se generan movimientos validos.
- Los hijos respetan la regla de no regresar para fantasmas.

### Paso 6: Implementar Alfa-Beta Generico

Implementar poda alfa-beta independiente del juego visual.

Criterio de exito:

- Alfa-beta puede recibir un estado inicial y devolver una accion.
- Se puede probar con una profundidad pequena, por ejemplo 2 o 3.

### Paso 7: Implementar Pinky

Crear evaluacion individual.

Funcion sugerida:

```text
score =
  - distancia_grafo(Pinky, PacMan)
  - penalizacion_tabu
  + bonus_por_reducir_distancia
```

Criterio de exito:

- Pinky deja de moverse aleatoriamente.
- Pinky tiende a acercarse a PacMan por caminos reales del laberinto.

### Paso 8: Implementar Tabu

Agregar memoria de ultimos nodos o estados.

Recomendacion:

- Horizonte inicial: 4 o 6 movimientos.
- Penalizar repetir nodos recientes.
- No bloquear completamente si no hay alternativa.

Criterio de exito:

- El fantasma evita ciclos cortos.
- El comportamiento se ve menos repetitivo.

### Paso 9: Implementar Inky Y Clyde Colaborativos

Crear estado con dos fantasmas.

Primera version recomendada:

- Accion conjunta: ambos eligen movimiento en el mismo nivel.

Ventaja:

- Es mas facil decir que hay colaboracion real.

Desventaja:

- Aumenta el numero de hijos.

Funcion sugerida:

```text
score =
  - min(dist(Inky, PacMan), dist(Clyde, PacMan))
  - 0.5 * (dist(Inky, PacMan) + dist(Clyde, PacMan))
  + cobertura_de_salidas
  + separacion_util
  - penalizacion_tabu
```

Criterio de exito:

- Los dos fantasmas no toman siempre el mismo camino.
- Uno puede acercarse y otro puede bloquear.

### Paso 10: Conectar IA Con Ghost.py

Modificar `Ghost.py` lo minimo posible.

Objetivo:

- Mantener `tipo=0` para aleatorio.
- Usar `tipo=1` para Pinky.
- Usar `tipo=2` o controlador compartido para Inky/Clyde.

Criterio de exito:

- Blinky sigue siendo aleatorio.
- Pinky usa alfa-beta.
- Inky/Clyde usan evaluacion colaborativa.

### Paso 11: Agregar Captura Y Metricas

Agregar una condicion simple:

```text
si distancia entre fantasma y PacMan es menor a cierto umbral, PacMan fue atrapado
```

Metricas sugeridas:

- Numero de pasos hasta captura.
- Profundidad usada.
- Nodos expandidos.
- Podas realizadas.
- Tiempo promedio de decision.

Criterio de exito:

- Se puede reportar eficiencia en el PDF.

### Paso 12: Documentar Para El Reporte

Crear documentos:

```text
docs/diseno_alfa_beta.md
docs/resultados_pruebas.md
Documentation/heuristics.md
```

Contenido minimo:

- Como se representa el laberinto.
- Como se representa el estado.
- Como se generan hijos.
- Pseudocodigo de alfa-beta.
- Heuristicas de Pinky.
- Heuristicas de Inky/Clyde.
- Explicacion de tabu.
- Resultados de pruebas.

### Paso 13: Preparar Video

Guion sugerido de menos de 5 minutos:

1. Mostrar el proyecto base.
2. Explicar controles.
3. Mostrar Blinky aleatorio.
4. Mostrar Pinky con alfa-beta.
5. Mostrar Inky/Clyde colaborativos.
6. Mostrar rapidamente el codigo modular.
7. Mencionar heuristicas y tabu.

## Riesgos Tecnicos

### Riesgo 1: Alfa-Beta Muy Lento

La busqueda puede crecer rapido.

Mitigacion:

- Usar profundidad pequena.
- Ordenar movimientos.
- Usar tabu.
- Pensar por intersecciones, no por pixeles.

### Riesgo 2: PacMan Manual Es Dificil De Modelar

PacMan es controlado por una persona real, pero alfa-beta necesita simular futuros movimientos.

Mitigacion:

- Modelar a PacMan como minimizador racional.
- O modelarlo como prediccion local basada en direccion actual.
- Explicar la decision en el reporte.

### Riesgo 3: Dos Fantasmas Colaborativos Generan Muchos Hijos

Si cada fantasma tiene 3 movimientos, una accion conjunta puede tener 9 combinaciones.

Mitigacion:

- Limitar profundidad.
- Ordenar movimientos por distancia.
- Podar con alfa-beta.
- Evitar acciones duplicadas o malas por heuristica.

### Riesgo 4: Romper El Proyecto Base

Modificar demasiado `main.py`, `Pacman.py` o `Ghost.py` puede romper el render.

Mitigacion:

- Agregar la IA en carpeta nueva.
- Hacer cambios pequenos en archivos existentes.
- Probar cada paso.

## Prioridad Inmediata

Estado actualizado:

```text
AI/__init__.py
AI/maze_graph.py
```

Estos archivos ya fueron creados para representar las intersecciones como un grafo reutilizable.

Validacion esperada del grafo derivado desde `MC`:

```text
66 nodos
170 aristas dirigidas
conectividad completa
0 aristas asimetricas
```

Tambien se agrego Dijkstra en `MazeGraph.shortest_distance()` para calcular distancias reales por el laberinto.

El siguiente paso recomendado ahora es crear:

```text
AI/game_state.py
```

Ese archivo debe representar los estados que usara alfa-beta para simular movimientos futuros.

Estado actualizado:

```text
AI/game_state.py
```

Ya fue creado con:

- `ActorState`
- `GameState`
- generacion de hijos para PacMan
- generacion de hijos para Pinky
- generacion de hijos conjunta para Inky/Clyde

Estado actualizado:

```text
AI/heuristics.py
```

Ya fue creado con la evaluacion inicial para Pinky:

- distancia real a PacMan usando Dijkstra
- numero de rutas de escape de PacMan
- penalizacion tabu con horizonte limitado

Tambien se agrego la evaluacion colaborativa para Inky/Clyde:

- distancia de ambos fantasmas a PacMan
- salidas cubiertas
- rutas libres de PacMan
- separacion util entre fantasmas
- penalizacion por cubrir la misma salida
- penalizacion tabu

Estado actualizado:

```text
AI/alpha_beta.py
```

Ya fue creado con:

- poda alfa-beta generica
- ordenamiento de movimientos
- deteccion de captura
- metricas de busqueda
- funcion `choose_pinky_action()` conectada con `Ghost.py` mediante `PinkyGhostController`
- funcion `choose_pack_action()` para Inky/Clyde
- tabu con horizonte limitado como penalizacion heuristica

Estado actualizado:

```text
AI/ghost_controller.py
```

Ya fue creado y conectado con los fantasmas inteligentes:

- `ghosts[0]`: Blinky rojo aleatorio
- `ghosts[1]`: Pinky rosa con alfa-beta
- `ghosts[2]`: Inky azul/cian con alfa-beta colaborativo
- `ghosts[3]`: Clyde naranja con alfa-beta colaborativo

Mapeo de imagenes observado:

- `fantasma4.bmp`: Blinky rojo
- `fantasma3.bmp`: Pinky rosa
- `fantasma2.bmp`: Inky azul/cian
- `fantasma1.bmp`: Clyde naranja

## Resumen De Lo Que Debemos Hacer A Continuacion

1. Probar visualmente los cuatro fantasmas.
2. Ajustar pesos de la heuristica colaborativa si Inky/Clyde se amontonan.
3. Revisar metricas visibles o logs de prueba.
4. Documentar pseudocodigo y resultados.
5. Preparar video final.

## Decision De Diseno Recomendada

La decision mas importante es que la IA debe operar por intersecciones, no por pixeles.

Esto no significa crear otro mapa distinto ni ignorar los archivos existentes. Al contrario: la razon de usar `MC`, `xMC`, `yMC`, `mapa.csv` y `mapa_codigos.csv` es precisamente simplificar el problema para que alfa-beta solo decida en puntos donde realmente hay una decision.

El movimiento grafico puede seguir ocurriendo pixel por pixel. Pero mientras un fantasma esta en un pasillo, no necesita volver a calcular una accion en cada pixel, porque no puede cambiar de direccion hasta llegar a la siguiente interseccion.

Motivos:

- Reduce el tamano del arbol de busqueda.
- Coincide con la regla del examen: solo cambiar direccion en intersecciones.
- Aprovecha la matriz `MC` ya existente.
- Aprovecha la informacion codificada en `mapa_codigos.csv`.
- Facilita calcular distancias reales del laberinto.
- Hace mas facil explicar alfa-beta en el reporte.

Flujo esperado:

```text
fantasma avanza por pixeles
        |
        v
llega a una interseccion
        |
        v
se consulta el grafo de intersecciones
        |
        v
alfa-beta decide la siguiente direccion
        |
        v
fantasma sigue por el pasillo hasta la siguiente interseccion
```

Por eso el trabajo pendiente no es inventar las intersecciones. Las intersecciones ya estan. El trabajo pendiente es convertirlas en una estructura facil de consultar para generar hijos, calcular costos y ejecutar alfa-beta.
