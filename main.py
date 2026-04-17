import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import os
import numpy as np
import pandas as pd

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Pacman import Pacman
from Ghost import Ghost
from IA import MazeControl, PackGhostController, PinkyGhostController


screen_width = 900
screen_height = 800
#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X = 200.0
EYE_Y = 460.0
EYE_Z = 200.0
CENTER_X = 0 + 200
CENTER_Y = 0
CENTER_Z = 0 + 200
UP_X=0
UP_Y=0
UP_Z=-1
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 400
#Variables para el control del observador
theta = 0.0
radius = 300
CAMERA_HEIGHT_STEP = 2.0
CAMERA_MIN_Y = 250.0
CAMERA_MAX_Y = 800.0


#Arreglo para el manejo de texturas
textures = []
#Nombre de los archivos a usar
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
file_1 = os.path.join(BASE_PATH, 'mapa.bmp')
img_pacman = os.path.join(BASE_PATH, 'pacman.bmp')
img_blinky = os.path.join(BASE_PATH, 'fantasma4.bmp') # rojo
img_pinky = os.path.join(BASE_PATH, 'fantasma3.bmp') # rosa
img_inky = os.path.join(BASE_PATH, 'fantasma2.bmp') # azul/cian
img_clyde = os.path.join(BASE_PATH, 'fantasma1.bmp') # naranja


file_csv = os.path.join(BASE_PATH, 'mapa.csv')
matrix = np.array(pd.io.parsers.read_csv(file_csv, header=None)).astype("int")
zmatrix = len(matrix)
xmatrix = len(matrix[0])


#Arreglos para imprimir intersecciones en el mapa del pacman
zarray = [-180 + 200, -128 + 200, -90 + 200, -50 + 200, -12 + 200, 28 + 200, 64 + 200, 102 + 200, 140 + 200, 180 + 200]
xarray = [-180 + 200, -150 + 200, -108 + 200, -65 + 200, -22 + 200, 21 + 200, 64 + 200, 107 + 200, 149 + 200, 178 + 200]

#Matriz de Control para mapeo entre pixeles <-> coord donde se localizan esquinas
MC = [
    [10,0,21,0,11,10,0,21,0,11],
    [24,0,25,21,23,23,21,25,0,22],
    [12,0,22,12,11,10,13,24,0,13],
    [0,0,0,10,23,23,11,0,0,0],
    [26,0,25,22,0,0,24,25,0,27],
    [0,0,0,24,0,0,22,0,0,0],
    [10,0,25,23,11,10,23,25,0,11],
    [12,11,24,21,23,23,21,22,10,13],
    [10,23,13,12,11,10,13,12,23,11],
    [12,0,0,0,23,23,0,0,0,13]
]

xMC = [0,30,71,114,156,199,242,286,328,358]

#XPxToMC = np.zeros((359,), dtype=int)
XPxToMC = np.full(359, -1, dtype=int)
XPxToMC[0] = 0
XPxToMC[30] = 1
XPxToMC[71] = 2
XPxToMC[114] = 3
XPxToMC[156] = 4
XPxToMC[199] = 5
XPxToMC[242] = 6
XPxToMC[286] = 7
XPxToMC[328] = 8
XPxToMC[358] = 9
 
yMC = [0,51,90,130,168,208,244,282,320,360]
#YPxToMC = np.zeros((361,), dtype=int)
YPxToMC = np.full(361, -1, dtype=int)
YPxToMC[0] = 0
YPxToMC[51] = 1
YPxToMC[90] = 2
YPxToMC[130] = 3
YPxToMC[168] = 4
YPxToMC[208] = 5
YPxToMC[244] = 6
YPxToMC[282] = 7
YPxToMC[320] = 8
YPxToMC[360] = 9

#Variables heredadas del proyecto base. No se usan para resolver la IA.
path = []
grid = []

# Logs detallados de busqueda apagados para no llenar la consola durante el juego.
DEBUG_AI_LOGS = False
AI_LOG_INTERVAL_FRAMES = 60
frame_count = 0
CAPTURE_LOGS = os.environ.get("PACMAN_CAPTURE_LOGS", "1") == "1"
CAPTURE_DISTANCE = 10
capture_count = 0
capture_round_start_ms = 0
active_capture_ghosts = set()
capture_type_counts = {
    "aleatorio": 0,
    "IA individual alpha-beta": 0,
    "caza en manada": 0,
}
ghost_capture_types = [
    ("Blinky", "aleatorio"),
    ("Pinky", "IA individual alpha-beta"),
    ("Inky", "caza en manada"),
    ("Clyde", "caza en manada"),
]

maze_control = MazeControl(MC, xMC, yMC)
pinky_controller = PinkyGhostController(maze_control, depth=4)
pack_controller = PackGhostController(maze_control, depth=3)

#pacman object
pc = Pacman(matrix, MC, XPxToMC, YPxToMC)
#fantasmas
ghosts = []
ghosts.append(Ghost(matrix, MC, XPxToMC, YPxToMC, 378, 380, 2, 0))
ghosts.append(Ghost(matrix, MC, XPxToMC, YPxToMC, 378, 20, 0, 1))
ghosts.append(Ghost(matrix, MC, XPxToMC, YPxToMC, 20, 380, 3, 1))
ghosts.append(Ghost(matrix, MC, XPxToMC, YPxToMC, 378, 188, 3, 1))
ghosts[1].setController(pinky_controller)
ghosts[2].setController(pack_controller, ghost_index=0)
ghosts[3].setController(pack_controller, ghost_index=1)

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def apply_border_black_transparency(image):
    # Elimina solo el negro conectado al borde de la imagen.
    # Asi no se borran detalles negros internos del sprite.
    pixels = pygame.surfarray.pixels3d(image)
    alpha = pygame.surfarray.pixels_alpha(image)
    width, height = image.get_size()
    visited = np.zeros((width, height), dtype=bool)
    stack = []

    for x in range(width):
        stack.append((x, 0))
        stack.append((x, height - 1))
    for y in range(height):
        stack.append((0, y))
        stack.append((width - 1, y))

    while stack:
        x, y = stack.pop()
        if visited[x, y]:
            continue
        visited[x, y] = True

        if not (
            pixels[x, y, 0] == 0 and
            pixels[x, y, 1] == 0 and
            pixels[x, y, 2] == 0
        ):
            continue

        alpha[x, y] = 0

        if x > 0:
            stack.append((x - 1, y))
        if x < width - 1:
            stack.append((x + 1, y))
        if y > 0:
            stack.append((x, y - 1))
        if y < height - 1:
            stack.append((x, y + 1))

    del pixels
    del alpha

def Texturas(filepath, transparent_border_black=False):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    if transparent_border_black:
        image = pygame.image.load(filepath).convert_alpha()
        apply_border_black_transparency(image)
    else:
        image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image,"RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    
def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    #textures[0]: plano
    Texturas(file_1)
    #textures[1]: pacman
    Texturas(img_pacman, transparent_border_black=True)
    #textures[2]: Blinky rojo
    Texturas(img_blinky, transparent_border_black=True)
    #textures[3]: Pinky rosa
    Texturas(img_pinky, transparent_border_black=True)
    #textures[4]: Inky azul/cian
    Texturas(img_inky, transparent_border_black=True)
    #textures[5]: Clyde naranja
    Texturas(img_clyde, transparent_border_black=True)

    #se pasan las texturas a los objetos
    pc.loadTextures(textures,1)
    ghosts[0].loadTextures(textures,2)
    ghosts[1].loadTextures(textures,3)
    ghosts[2].loadTextures(textures,4)
    ghosts[3].loadTextures(textures,5)
    
def PlanoTexturizado():
    #Activate textures
    glColor3f(1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)
    #front face
    glBindTexture(GL_TEXTURE_2D, textures[0])    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(0, 0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(0, 0, DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoard, 0, DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoard, 0, 0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

#Se mueve al observador circularmente al rededor del plano XZ
def lookat():
    global EYE_X
    global EYE_Y
    global EYE_Z
    global UP_X
    global UP_Z
    global radius
    center = DimBoard / 2
    # Vista cenital: la camara se queda sobre el centro del tablero.
    EYE_X = center
    EYE_Z = center
    # Desde arriba, el vector UP no puede apuntar en Y porque queda alineado
    # con la direccion de la mirada. Se rota en XZ para conservar las flechas.
    UP_X = math.sin(math.radians(theta))
    UP_Z = -math.cos(math.radians(theta))
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

def display():
    global frame_count
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    PlanoTexturizado()
    pc.draw()
    pack_controller.set_pack_snapshot(
        ghosts[2].position,
        ghosts[2].direction,
        ghosts[3].position,
        ghosts[3].direction,
        pc.position,
        pc.direction,
    )
    for g in ghosts:
        g.draw()
        g.update2(pc.position, pc.direction)
    log_ai_decisions()
    log_capture_events()
    frame_count += 1

def is_capture_distance(ghost):
    return (
        abs(ghost.position[0] - pc.position[0]) <= CAPTURE_DISTANCE and
        abs(ghost.position[2] - pc.position[2]) <= CAPTURE_DISTANCE
    )

def log_capture_events():
    global capture_count
    global capture_round_start_ms

    if not CAPTURE_LOGS:
        return

    current_captures = {
        index
        for index, ghost in enumerate(ghosts)
        if is_capture_distance(ghost)
    }
    new_captures = current_captures - active_capture_ghosts

    if new_captures:
        capture_count += 1
        now_ms = pygame.time.get_ticks()
        elapsed_seconds = (now_ms - capture_round_start_ms) / 1000
        capture_ghosts = [
            ghost_capture_types[ghost_index]
            for ghost_index in sorted(new_captures)
        ]
        ghost_names = [name for name, _ in capture_ghosts]
        ghost_types = sorted({ghost_type for _, ghost_type in capture_ghosts})

        for ghost_type in ghost_types:
            capture_type_counts[ghost_type] += 1

        print(
            "[CAPTURE] "
            f"total={capture_count} "
            f"ghosts={','.join(ghost_names)} "
            f"types={','.join(ghost_types)} "
            f"time={elapsed_seconds:.2f}s "
            f"frame={frame_count} "
            f"pacman_pos={pc.position} "
            f"type_counts={capture_type_counts}"
        )
        capture_round_start_ms = now_ms

    active_capture_ghosts.clear()
    active_capture_ghosts.update(current_captures)

def format_search_stats(stats):
    if stats is None:
        return "stats=None"
    return (
        f"nodes={stats.nodes_expanded} "
        f"leaves={stats.leaves_evaluated} "
        f"alpha_cuts={stats.alpha_cuts} "
        f"beta_cuts={stats.beta_cuts} "
        f"depth={stats.max_depth_reached} "
        f"aspiration={stats.aspiration_searches} "
        f"research={stats.aspiration_researches} "
        f"continuations={stats.heuristic_continuations}"
    )

def log_ai_decisions():
    if not DEBUG_AI_LOGS:
        return
    if frame_count % AI_LOG_INTERVAL_FRAMES != 0:
        return

    pinky_components = pinky_controller.last_components
    pack_components = pack_controller.last_components
    print(
        "[AI][State] "
        f"frame={frame_count} "
        f"pacman_pos={pc.position} pacman_dir={pc.direction} "
        f"blinky_pos={ghosts[0].position} blinky_dir={ghosts[0].direction} "
        f"pinky_pos={ghosts[1].position} pinky_dir={ghosts[1].direction} "
        f"inky_pos={ghosts[2].position} inky_dir={ghosts[2].direction} "
        f"clyde_pos={ghosts[3].position} clyde_dir={ghosts[3].direction}"
    )
    print(
        "[AI][Pinky] "
        f"action={pinky_controller.last_action} "
        f"value={pinky_controller.last_value} "
        f"{format_search_stats(pinky_controller.last_stats)} "
        f"components={pinky_components}"
    )
    print(
        "[AI][Pack] "
        f"action={pack_controller.last_action} "
        f"value={pack_controller.last_value} "
        f"{format_search_stats(pack_controller.last_stats)} "
        f"components={pack_components}"
    )

def run_game():
    global EYE_Y
    global theta
    global capture_round_start_ms

    done = False
    pygame.init()
    capture_round_start_ms = pygame.time.get_ticks()
    Init()
    #finding(matrix, (xarray[0]-20,zarray[0]-20), (xarray[9]-20,zarray[9]-20))
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if theta > 359.0:
                theta = 0
            else:
                theta += 1.0
            lookat()
        if keys[pygame.K_LEFT]:
            if theta < 1.0:
                theta = 360.0
            else:
                theta += -1.0
            lookat()
        if keys[pygame.K_UP]:
            EYE_Y = min(EYE_Y + CAMERA_HEIGHT_STEP, CAMERA_MAX_Y)
            lookat()
        if keys[pygame.K_DOWN]:
            EYE_Y = max(EYE_Y - CAMERA_HEIGHT_STEP, CAMERA_MIN_Y)
            lookat()
        #Se verifica la direccion para el pacman
        pacman_dir = -1
        if keys[pygame.K_w]:
            #direccion 0
            pacman_dir = 0
        elif keys[pygame.K_d]:
            #direccion 1
            pacman_dir = 1
        elif keys[pygame.K_s]:
            #direccion 2
            pacman_dir = 2
        elif keys[pygame.K_a]:
            #direccion 1
            pacman_dir = 3
        pc.updateWithBuffer(pacman_dir)

        display()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    run_game()
    

