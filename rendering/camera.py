import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math


class Camera:
    """Gestiona la cámara y las matrices de proyección"""
    
    def __init__(self, display_width, display_height):
        self.position = np.array([0.0, 2.0, 8.0], dtype=np.float32)
        
        self.view = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, -2],
            [0, 0, 1, -8],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        aspect = display_width / display_height
        fov = 45.0 * math.pi / 180.0
        near, far = 0.1, 100.0
        f = 1.0 / math.tan(fov / 2.0)
        
        self.projection = np.array([
            [f/aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
            [0, 0, -1, 0]
        ], dtype=np.float32)
