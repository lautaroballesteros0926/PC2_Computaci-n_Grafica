import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math


class SphereGeometry:
    """Genera y gestiona la geometría de una esfera"""
    
    def __init__(self, radius=1.0, sectors=48, stacks=24):
        self.radius = radius
        self.sectors = sectors
        self.stacks = stacks
        self.vertices, self.indices = self._create_sphere()
        self.vao, self.index_count = self._setup_vao()
    
    def _create_sphere(self):
        """Genera vértices e índices de la esfera"""
        vertices = []
        indices = []
        
        for i in range(self.stacks + 1):
            stack_angle = math.pi / 2 - i * math.pi / self.stacks
            xy = self.radius * math.cos(stack_angle)
            z = self.radius * math.sin(stack_angle)
            
            for j in range(self.sectors + 1):
                sector_angle = j * 2 * math.pi / self.sectors
                
                x = xy * math.cos(sector_angle)
                y = xy * math.sin(sector_angle)
                
                nx = x / self.radius
                ny = y / self.radius
                nz = z / self.radius
                
                s = j / self.sectors
                t = i / self.stacks
                
                vertices.extend([x, y, z, nx, ny, nz, s, t])
        
        for i in range(self.stacks):
            k1 = i * (self.sectors + 1)
            k2 = k1 + self.sectors + 1
            
            for j in range(self.sectors):
                if i != 0:
                    indices.extend([k1, k2, k1 + 1])
                if i != (self.stacks - 1):
                    indices.extend([k1 + 1, k2, k2 + 1])
                k1 += 1
                k2 += 1
        
        return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)
    
    def _setup_vao(self):
        """Configura el VAO para la esfera"""
        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        ebo = glGenBuffers(1)
        
        glBindVertexArray(vao)
        
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        
        # Position
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Normal
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        
        # TexCoord
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)
        
        glBindVertexArray(0)
        
        return vao, len(self.indices)
