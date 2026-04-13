# Camera Controls Update

## Summary

The camera controls were updated so the project can move the observer vertically with the keyboard.

Before this change, only the left and right arrow keys were handled. They rotated the camera around the PacMan board by changing the horizontal camera angle.

After this change:

- Left arrow: rotates the camera to the left.
- Right arrow: rotates the camera to the right.
- Up arrow: raises the camera.
- Down arrow: lowers the camera.

PacMan movement is still controlled with:

- W: move up.
- A: move left.
- S: move down.
- D: move right.

## Modified File

The change was made in:

```text
main.py
```

## Implementation Details

Three constants were added for vertical camera movement:

```python
CAMERA_HEIGHT_STEP = 2.0
CAMERA_MIN_Y = 20.0
CAMERA_MAX_Y = 500.0
```

The `lookat()` function now includes `EYE_Y` as a global variable because the vertical camera height can change while the game is running.

The main game loop now checks for:

```python
pygame.K_UP
pygame.K_DOWN
```

When the up arrow is pressed, `EYE_Y` increases until it reaches `CAMERA_MAX_Y`.

When the down arrow is pressed, `EYE_Y` decreases until it reaches `CAMERA_MIN_Y`.

## How To Test

Run the project with the virtual environment:

```bash
.venv/bin/python main.py
```

Then use:

```text
Left arrow / Right arrow: rotate camera
Up arrow / Down arrow: change camera height
W / A / S / D: move PacMan
ESC: close the game
```

## Commit

This change was committed as:

```text
c12d961 Add vertical camera controls
```
