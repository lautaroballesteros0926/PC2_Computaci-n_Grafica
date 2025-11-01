import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
from rendering.transform import Transform

class Renderer3D:
    """Gestiona el renderizado OpenGL de las esferas"""
    
    def __init__(self, shader_program, sphere_geometry, camera):
        self.shader_program = shader_program
        self.sphere = sphere_geometry
        self.camera = camera
        self.light_pos = [5.0, 5.0, 5.0]
        self.light_color = [1.0, 1.0, 1.0]
    
    def render_sphere(self, material, position, rotation_angle):
        """Renderiza una esfera con un material específico"""
        model = Transform.create_model_matrix(
            position[0], position[1], position[2],
            0, rotation_angle * 0.02, rotation_angle * 0.01,
            1.2, 1.2, 1.2
        )
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "model"), 1, GL_TRUE, model)
        
        glUniform3fv(glGetUniformLocation(self.shader_program, "materialAmbient"), 1, material.ambient)
        glUniform3fv(glGetUniformLocation(self.shader_program, "materialDiffuse"), 1, material.diffuse)
        glUniform3fv(glGetUniformLocation(self.shader_program, "materialSpecular"), 1, material.specular)
        glUniform1f(glGetUniformLocation(self.shader_program, "materialShininess"), material.shininess)
        glUniform1f(glGetUniformLocation(self.shader_program, "materialReflectivity"), material.reflectivity)
        glUniform1i(glGetUniformLocation(self.shader_program, "materialType"), material.material_type)
        
        glDrawElements(GL_TRIANGLES, self.sphere.index_count, GL_UNSIGNED_INT, None)
    
    def setup_uniforms(self):
        """Configura los uniforms del shader"""
        glUniform3fv(glGetUniformLocation(self.shader_program, "lightPos"), 1, self.light_pos)
        glUniform3fv(glGetUniformLocation(self.shader_program, "viewPos"), 1, self.camera.position)
        glUniform3fv(glGetUniformLocation(self.shader_program, "lightColor"), 1, self.light_color)
        
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "view"), 1, GL_TRUE, self.camera.view)
        glUniformMatrix4fv(glGetUniformLocation(self.shader_program, "projection"), 1, GL_TRUE, self.camera.projection)