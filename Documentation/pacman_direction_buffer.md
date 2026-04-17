# PacMan Direction Buffer

## Objetivo

Se agrego un buffer de direccion para PacMan.

La finalidad es que el jugador pueda presionar `W`, `A`, `S` o `D` un poco antes de llegar a una interseccion. La direccion se guarda temporalmente y se ejecuta cuando PacMan llega a un punto donde puede girar.

Esto mejora el control porque el jugador ya no necesita presionar la tecla exactamente en el pixel de la interseccion.

## Problema Que Resuelve

Antes del cambio, PacMan solo podia girar si la tecla se detectaba justo cuando estaba en una interseccion valida.

Ejemplo:

```text
PacMan avanza hacia la derecha.
El jugador quiere girar hacia arriba.
Si presiona W unos pixeles antes de la interseccion, el giro podia perderse.
```

Con el buffer:

```text
PacMan avanza hacia la derecha.
El jugador presiona W antes de llegar a la interseccion.
La direccion W queda guardada por una distancia limitada.
Cuando PacMan llega a la interseccion, intenta girar hacia arriba.
```

## Regla Principal

La orden del jugador no se guarda para siempre.

Se guarda solo hasta que ocurra una de estas condiciones:

- PacMan logra usar la direccion en una interseccion.
- PacMan avanza mas de la distancia permitida desde que se presiono la tecla.
- El jugador presiona otra direccion y reemplaza la anterior.

## Limite Por Distancia

Se uso limite por distancia, no por frames.

Esto significa que la orden dura cierta cantidad de pixeles recorridos por PacMan.

Valor actual:

```python
self.buffer_max_distance = 45
```

Este valor permite presionar una direccion poco antes de una interseccion, pero evita que una orden vieja se ejecute mucho despues.

## Archivos Modificados

```text
Pacman.py
main.py
```

## Cambios En Pacman.py

Se agregaron estos atributos:

```python
self.buffered_direction = -1
self.buffer_start_position = None
self.buffer_max_distance = 45
```

`buffered_direction` guarda la direccion pendiente.

`buffer_start_position` guarda la posicion donde se presiono la tecla.

`buffer_max_distance` define cuantos pixeles puede durar la orden.

Tambien se agregaron estos metodos:

```python
bufferDirection(dir)
clearDirectionBuffer()
getBufferedDirection()
updateWithBuffer(dir)
```

## Funcionamiento General

Flujo de control:

```text
1. main.py lee la tecla presionada.
2. main.py manda esa direccion a PacMan.
3. PacMan guarda la direccion como pendiente.
4. En cada actualizacion, PacMan revisa si la direccion sigue vigente.
5. Si llega a una interseccion valida, intenta usarla.
6. Si el giro se logra, el buffer se limpia.
7. Si PacMan avanza demasiado sin usarla, el buffer expira.
```

## Direcciones Del Proyecto

El proyecto usa estos codigos:

```text
0 = arriba
1 = derecha
2 = abajo
3 = izquierda
-1 = sin direccion nueva
```

## Cambios En main.py

Antes, `main.py` llamaba directamente a:

```python
pc.update(0)
pc.update(1)
pc.update(2)
pc.update(3)
pc.update(-1)
```

Ahora primero calcula la direccion solicitada:

```python
pacman_dir = -1
```

Y despues llama:

```python
pc.updateWithBuffer(pacman_dir)
```

Eso permite que `Pacman.py` controle si la direccion se usa inmediatamente, se guarda temporalmente o expira.

## Relacion Con La IA

Este cambio no pertenece directamente al modulo `IA`.

Es una mejora del control del jugador, por eso se implemento en `Pacman.py`.

La carpeta `IA` debe reservarse para:

- matriz de control del laberinto,
- generacion de hijos,
- poda alfa-beta,
- heuristicas,
- tabu,
- coordinacion de fantasmas.

El buffer de PacMan ayuda indirectamente a la IA porque hace mas claro el estado del jugador:

```text
direccion actual
direccion pendiente temporal
posicion actual
```

## Como Probar

Ejecutar el proyecto:

```bash
.venv/bin/python main.py
```

Prueba sugerida:

```text
1. Mueve PacMan hacia la derecha con D.
2. Antes de llegar a una interseccion donde pueda subir, presiona W.
3. PacMan debe girar hacia arriba si la interseccion esta dentro del limite del buffer.
4. Presiona una direccion demasiado lejos de una interseccion.
5. La orden debe expirar y no ejecutarse mucho despues.
```

## Valor Ajustable

Si el buffer se siente muy corto o muy largo, ajustar:

```python
self.buffer_max_distance = 45
```

Valores recomendados para probar:

```text
30 = mas estricto
45 = balanceado
60 = mas permisivo
```
