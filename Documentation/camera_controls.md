# Camera Controls

## Objetivo

Este documento describe el estado actual de la camara del proyecto.

La camara esta configurada como vista cenital para observar el tablero desde arriba.

## Archivo Modificado

```text
main.py
```

## Valores Actuales

```python
EYE_X = 200.0
EYE_Y = 460.0
EYE_Z = 200.0
CENTER_X = 200
CENTER_Y = 0
CENTER_Z = 200
UP_X = 0
UP_Y = 0
UP_Z = -1
```

`EYE_Y` controla que tan cerca esta la camara del tablero:

- valor menor: camara mas cercana,
- valor mayor: camara mas alejada.

Limites actuales:

```python
CAMERA_HEIGHT_STEP = 2.0
CAMERA_MIN_Y = 250.0
CAMERA_MAX_Y = 800.0
```

## Por Que `UP_Y` Es Cero

En una vista desde arriba, la camara mira hacia abajo en el eje Y.

Si `UP_Y` tambien apuntara en Y, el vector de arriba quedaria alineado con la direccion de vision y OpenGL podria calcular mal la orientacion.

Por eso se usa:

```python
UP_Y = 0
UP_Z = -1
```

La funcion `lookat()` rota `UP_X` y `UP_Z` para conservar la rotacion de la vista con las flechas izquierda y derecha.

## Controles Actuales

```text
Flecha izquierda  -> rota la orientacion de la vista desde arriba
Flecha derecha    -> rota la orientacion de la vista desde arriba
Flecha arriba     -> aleja/sube la camara
Flecha abajo      -> acerca/baja la camara
W                 -> mueve PacMan hacia arriba
A                 -> mueve PacMan hacia la izquierda
S                 -> mueve PacMan hacia abajo
D                 -> mueve PacMan hacia la derecha
ESC               -> cierra el juego
```

## Relacion Con Los Sprites

PacMan y los fantasmas mantienen su posicion logica en `Y = 1`.

Para que se vean desde la vista cenital, se dibujan visualmente un poco mas arriba:

```python
SPRITE_DRAW_Y = 8
```

Esto no cambia la IA ni el movimiento. Solo evita que el plano del mapa los tape visualmente.

## Como Probar

Ejecutar:

```bash
.venv/bin/python main.py
```

Comprobar:

- el tablero se ve desde arriba,
- PacMan y fantasmas se ven sobre el mapa,
- las flechas izquierda/derecha rotan la orientacion,
- las flechas arriba/abajo cambian la altura,
- `W`, `A`, `S`, `D` siguen controlando PacMan.
