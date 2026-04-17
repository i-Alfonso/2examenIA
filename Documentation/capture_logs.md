# Capture Logs

## Objetivo

Los logs detallados de busqueda alfa-beta estan apagados para no llenar la consola durante la ejecucion normal.

En su lugar, se agrego un log especifico de capturas. Este log solo imprime cuando algun fantasma alcanza a PacMan.

## Archivo Modificado

```text
main.py
```

## Logs De IA

Los logs detallados de busqueda estan apagados:

```python
DEBUG_AI_LOGS = False
```

Esto evita imprimir continuamente:

```text
[AI][State]
[AI][Pinky]
[AI][Pack]
```

## Logs De Captura

Los logs de captura estan activos por defecto:

```python
CAPTURE_LOGS = os.environ.get("PACMAN_CAPTURE_LOGS", "1") == "1"
```

Para apagarlos:

```bash
PACMAN_CAPTURE_LOGS=0 .venv/bin/python main.py
```

## Distancia De Captura

La captura se registra si el centro del fantasma esta cerca del centro de PacMan:

```python
CAPTURE_DISTANCE = 10
```

Se compara la distancia en X y Z:

```text
abs(ghost.x - pacman.x) <= CAPTURE_DISTANCE
abs(ghost.z - pacman.z) <= CAPTURE_DISTANCE
```

## Tipos De Fantasma

```text
Blinky -> aleatorio
Pinky  -> IA individual alpha-beta
Inky   -> caza en manada
Clyde  -> caza en manada
```

## Formato Del Log

Ejemplo:

```text
[CAPTURE] total=1 ghosts=Blinky types=aleatorio time=1.50s frame=123 pacman_pos=[100, 1, 100] type_counts={'aleatorio': 1, 'IA individual alpha-beta': 0, 'caza en manada': 0}
```

Campos:

```text
total
  capturas totales registradas.

ghosts
  fantasma o fantasmas que capturaron.

types
  tipo de estrategia del fantasma capturador.

time
  tiempo desde el inicio de la partida o desde la captura anterior.

frame
  frame en el que ocurrio la captura.

pacman_pos
  posicion de PacMan al momento de la captura.

type_counts
  conteo acumulado por tipo de estrategia.
```

## Capturas Simultaneas

Si Inky y Clyde capturan en el mismo frame, se registra como una sola captura de tipo:

```text
caza en manada
```

Ejemplo:

```text
[CAPTURE] total=1 ghosts=Inky,Clyde types=caza en manada time=2.30s frame=250 pacman_pos=[200, 1, 200] type_counts={'aleatorio': 0, 'IA individual alpha-beta': 0, 'caza en manada': 1}
```

## Evitar Duplicados

Si un fantasma queda encima de PacMan durante varios frames, la captura se cuenta una sola vez.

Para volver a contar, primero debe separarse y despues capturar de nuevo.
