import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

class Transform:
    """Gestiona las transformaciones de objetos"""
    
    @staticmethod
    def create_model_matrix(tx, ty, tz, rx, ry, rz, sx, sy, sz):
        """Crea una matriz de transformación modelo"""
        translation = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        cx, sx_r = math.cos(rx), math.sin(rx)
        cy, sy_r = math.cos(ry), math.sin(ry)
        cz, sz_r = math.cos(rz), math.sin(rz)
        
        rotation = np.array([
            [cy*cz, -cy*sz_r, sy_r, 0],
            [cx*sz_r + sx_r*sy_r*cz, cx*cz - sx_r*sy_r*sz_r, -sx_r*cy, 0],
            [sx_r*sz_r - cx*sy_r*cz, sx_r*cz + cx*sy_r*sz_r, cx*cy, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        scale = np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        return translation @ rotation @ scale