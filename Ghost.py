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
import random

class Ghost:
    SPRITE_DRAW_Y = 8

    def __init__(self,mapa, mc, x_mc, y_mc, xini, yini, dir, tipo):
        #Matriz de control que almacena los IDs de las intersecciones
        self.MC = mc
        #Vectores que almacenan las coordenadas 
        self.XPxToMC = x_mc
        self.YPxToMC = y_mc
        #se resplanda el mapa en terminos de pixeles
        self.mapa = mapa
        #se inicializa la posicion del fantasma en terminos de pixeles
        self.position = []
        self.position.append(xini)
        self.position.append(1) #YPos
        self.position.append(yini)
        #se define el arreglo para la posicion en la matriz de control
        self.positionMC = []
        self.positionMC.append(self.XPxToMC[self.position[0] - 20]) #coord en x
        self.positionMC.append(self.YPxToMC[self.position[2] - 20]) #coord en y
        #se inicializa una direccion valida
        self.direction = dir
        #se almacena que tipo de fantasma sera:
        #0: fantasma aleatorio
        #1: fantasma con pathfinding
        self.tipo = tipo
        #arreglo para almacenar las opciones del fantasma
        self.options = [
            [1,2],
            [2,3],
            [0,1],
            [0,3],
            [1,2,3],
            [0,2,3],
            [0,1,3],
            [0,1,2],
            [0,1,2,3],
            [1],
            [3]
        ]
        self.allowed_directions_by_cell = {
            10: [1, 2],
            11: [2, 3],
            12: [0, 1],
            13: [0, 3],
            21: [1, 2, 3],
            22: [0, 2, 3],
            23: [0, 1, 3],
            24: [0, 1, 2],
            25: [0, 1, 2, 3],
            26: [1],
            27: [3],
        }
        self.option = []
        self.dir_inv = 0
        self.controller = None
        self.controller_index = None
        self.path_n = 0
        self.valid_path_positions = self.build_valid_path_positions()

    def loadTextures(self, texturas, id):
        self.texturas = texturas
        self.Id = id

    def setController(self, controller, ghost_index=None):
        self.controller = controller
        self.controller_index = ghost_index

    # Sirve para validar que una posicion siga dentro del tablero antes de mover.
    def is_inside_board_position(self, x, z):
        x_index = x - 20
        z_index = z - 20
        return (
            0 <= x_index < len(self.XPxToMC) and
            0 <= z_index < len(self.YPxToMC)
        )

    # Sirve para reconstruir los pasillos validos usando MC.
    def build_valid_path_positions(self):
        x_coords = [
            pixel
            for pixel, column in enumerate(self.XPxToMC)
            if column != -1
        ]
        y_coords = [
            pixel
            for pixel, row in enumerate(self.YPxToMC)
            if row != -1
        ]

        path_positions = set()
        direction_deltas = {
            0: (-1, 0),
            1: (0, 1),
            2: (1, 0),
            3: (0, -1),
        }

        for row, cells in enumerate(self.MC):
            for col, cell_id in enumerate(cells):
                if cell_id == 0:
                    continue

                origin_x = x_coords[col] + 20
                origin_z = y_coords[row] + 20
                path_positions.add((origin_x, origin_z))

                for direction in self.allowed_directions_by_cell[cell_id]:
                    row_delta, col_delta = direction_deltas[direction]
                    next_row = row + row_delta
                    next_col = col + col_delta

                    while (
                        0 <= next_row < len(self.MC) and
                        0 <= next_col < len(self.MC[next_row])
                    ):
                        if self.MC[next_row][next_col] != 0:
                            target_x = x_coords[next_col] + 20
                            target_z = y_coords[next_row] + 20

                            if origin_x == target_x:
                                start = min(origin_z, target_z)
                                end = max(origin_z, target_z)
                                for z in range(start, end + 1):
                                    path_positions.add((origin_x, z))
                            elif origin_z == target_z:
                                start = min(origin_x, target_x)
                                end = max(origin_x, target_x)
                                for x in range(start, end + 1):
                                    path_positions.add((x, origin_z))
                            break

                        next_row += row_delta
                        next_col += col_delta

        return path_positions

    # Sirve para calcular a que pixel llegaria el fantasma si toma una direccion.
    def next_pixel_for_direction(self, direction):
        next_x = self.position[0]
        next_z = self.position[2]
        if direction == 0:
            next_z -= 1
        elif direction == 1:
            next_x += 1
        elif direction == 2:
            next_z += 1
        elif direction == 3:
            next_x -= 1
        return next_x, next_z

    # Sirve para evitar que una direccion saque al fantasma del tablero.
    def can_move_direction(self, direction):
        next_x, next_z = self.next_pixel_for_direction(direction)
        return (
            self.is_inside_board_position(next_x, next_z) and
            (next_x, next_z) in self.valid_path_positions
        )

    def drawFace(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x1, y1, z1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x2, y2, z2)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(x3, y3, z3)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(x4, y4, z4)
        glEnd()
   
    def sigue_adelante(self):
        #si el fantasma esta en un tunel, no es necesario calcular la siguiente posicion a traves del path
        #solo se sigue la direccion actual y se aumenta el contador que accede a la posicion del path actual
        self.move_direction(self.direction)
        #se actualiza la variable de posicion sobre el path
        if self.tipo == 1: #fantasma inteligente
            self.path_n += 1

    def move_direction(self, direction):
        if not self.can_move_direction(direction):
            return False

        self.direction = direction
        next_x, next_z = self.next_pixel_for_direction(direction)
        self.position[0] = next_x
        self.position[2] = next_z
        return True

    def path_ia(self,pacmanXY,pacman_dir):
        # bloque para implementar la IA en los fantasmas
        if self.controller is None:
            self.interseccion_random()
            return

        try:
            next_direction = self.controller.next_direction(
                self.position,
                self.direction,
                pacmanXY,
                pacman_dir,
                ghost_index=self.controller_index,
            )
        except ValueError:
            next_direction = None

        if next_direction is None or not self.can_move_direction(next_direction):
            self.interseccion_random()
        else:
            self.move_direction(next_direction)
        
    def interseccion_random(self):
        #se determina en que tipo de celda esta el fantasma
        self.positionMC[0] = self.XPxToMC[self.position[0] - 20]
        self.positionMC[1] = self.YPxToMC[self.position[2] - 20]
        celId = self.MC[self.positionMC[1]][self.positionMC[0]]
        #a partir de la celda actual se generan sus opciones posibles
        if celId == 0:
            self.option = [self.direction]
        elif celId == 10: #options = [1, 2]
            self.option = self.options[0].copy()
        elif celId == 11: #options = [2, 3]
            self.option = self.options[1].copy()
        elif celId == 12: #options = [0, 1]
            self.option = self.options[2].copy()
        elif celId == 13: #options = [0, 3]
            self.option = self.options[3].copy()
        elif celId == 21: #options = [1, 2, 3]
            self.option = self.options[4].copy()
        elif celId == 22: #options = [0, 2, 3]
            self.option = self.options[5].copy()
        elif celId == 23: #options = [0, 1, 3]
            self.option = self.options[6].copy()
        elif celId == 24: #options = [0, 1, 2]
            self.option = self.options[7].copy()
        elif celId == 25: #options = [0, 1, 2, 3]
            self.option = self.options[8].copy()
        elif celId == 26: #options = [1]
            self.option = self.options[9].copy()
        elif celId == 27: #options = [3]
            self.option = self.options[10].copy()
        
        #se calcula la direccion inversa a la actual
        if self.direction == 0:
            self.dir_inv = 2
        elif self.direction == 1:
            self.dir_inv = 3
        elif self.direction == 2:
            self.dir_inv = 0
        else:
            self.dir_inv = 1

        #se elimina la direccion invertida a la actual, evitando que el
        #fantasma regrese por el camion por donde llego (rebote)
        if ((celId != 0) and (celId != 26) and (celId != 27) and
            (self.dir_inv in self.option)):
            self.option.remove(self.dir_inv)

        self.option = [
            direction for direction in self.option
            if self.can_move_direction(direction)
        ]

        if not self.option and self.can_move_direction(self.dir_inv):
            self.option = [self.dir_inv]

        if not self.option:
            return

        #se elige aleatoriamente una opcion entre las disponibles
        size = len(self.option)
        dir_rand = random.randint(0, size - 1)
        
        #se actualiza el vector de direccion y posicion del fantasma
        self.move_direction(self.option[dir_rand])

    def update2(self,pacmanXY,pacman_dir=1):
        #si el fantasma se encuentra en una interseccion (valida o "falsa interseccion")
        if ((self.is_inside_board_position(self.position[0], self.position[2])) and
            (self.YPxToMC[self.position[2] - 20] != -1) and
            (self.XPxToMC[self.position[0] - 20] != -1)):
            if self.tipo == 1: #agente inteligente, se manda la posición del objetivo
                self.path_ia(pacmanXY,pacman_dir)
            else:
                self.interseccion_random()
        else: #si no se encuentra en una interseccion o es falsa interseccion
            self.sigue_adelante()
        
    def draw(self):
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        # Se dibuja un poco arriba del plano para que la vista cenital no lo tape.
        glTranslatef(self.position[0], self.SPRITE_DRAW_Y, self.position[2])
        glScaled(10,1,10)
        #Activate textures
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_GREATER, 0.5)
        #front face
        glBindTexture(GL_TEXTURE_2D, self.texturas[self.Id])
        self.drawFace(-1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0)
        glDisable(GL_ALPHA_TEST)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
