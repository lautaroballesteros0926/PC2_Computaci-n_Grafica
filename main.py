from shaders.shader_manager import ShaderManager
from geometry.sphere import SphereGeometry
from materials.material_library import MaterialLibrary
from rendering.camera import Camera
from rendering.renderer3d import Renderer3D
from ui.button import Button
from ui.ui_renderer import UIRenderer
import pygame
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

class Application:
    """Clase principal que gestiona la aplicación"""
    
    def __init__(self):
        pygame.init()
        self.display = (1200, 800)
        self.screen = pygame.display.set_mode(self.display)
        pygame.display.set_caption("Práctica Calificada 2 - Renderizado de Esferas")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Estado de la aplicación
        self.in_menu = True
        self.opengl_initialized = False
        self.view_mode = 0
        self.rotation_speed = 1.0
        self.paused = False
        self.rotation_angle = 0
        
        # Recursos OpenGL (se inicializan más tarde)
        self.shader_program = None
        self.sphere = None
        self.camera = None
        self.renderer = None
        self.materials = None
        
        # UI
        self.ui_surface = pygame.Surface(self.display, pygame.SRCALPHA)
        self.setup_buttons()
    
    def setup_buttons(self):
        """Configura los botones de la interfaz"""
        self.menu_buttons = [
            Button(400, 450, 400, 60, "INICIAR VISUALIZACIÓN", self.start_viewer)
        ]
        
        self.viewer_buttons = [
            Button(920, 520, 260, 45, "Todas las Esferas", lambda: self.set_view_mode(0)),
            Button(920, 575, 260, 45, "Esfera Metálica", lambda: self.set_view_mode(1)),
            Button(920, 630, 260, 45, "Esfera de Agua", lambda: self.set_view_mode(2)),
            Button(920, 685, 260, 45, "Esfera Opaca", lambda: self.set_view_mode(3))
        ]
    
    def start_viewer(self):
        """Inicia el modo visualizador 3D"""
        self.in_menu = False
        if not self.opengl_initialized:
            self.initialize_opengl()
    
    def initialize_opengl(self):
        """Inicializa los recursos de OpenGL"""
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        
        # DOUBLEBUF permite doble buffer para evitar parpadeos.
        # GL_DEPTH_TEST asegura el orden correcto de los objetos (ocultamiento por profundidad).
        # GL_MULTISAMPLE suaviza los bordes (anti-aliasing).
        
        # Carga de shaders, geometría y cámara
        self.shader_program = ShaderManager.create_program()
        self.sphere = SphereGeometry()
        self.camera = Camera(self.display[0], self.display[1])
        self.renderer = Renderer3D(self.shader_program, self.sphere, self.camera)
        self.materials = MaterialLibrary.get_materials()
        
        self.opengl_initialized = True
    
    def set_view_mode(self, mode):
        """Cambia el modo de visualización"""
        self.view_mode = mode
    
    def handle_events(self):
        """Maneja los eventos de entrada"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                self.handle_keydown(event.key)
            
            # Manejar eventos de botones
            if self.in_menu:
                for button in self.menu_buttons:
                    button.handle_event(event)
            else:
                for button in self.viewer_buttons:
                    button.handle_event(event)
    
    def handle_keydown(self, key):
        """Maneja las teclas presionadas"""
        if key == K_ESCAPE:
            self.running = False
        elif not self.in_menu:
            if key == K_m:
                self.in_menu = True
            elif key == K_PLUS or key == K_EQUALS:
                self.rotation_speed = min(5.0, self.rotation_speed + 0.5)
            elif key == K_MINUS:
                self.rotation_speed = max(0.0, self.rotation_speed - 0.5)
            elif key == K_SPACE:
                self.paused = not self.paused
            elif key == K_r:
                self.rotation_angle = 0
    
    def update(self):
        """Actualiza el estado de la aplicación"""
        if not self.in_menu and not self.paused:
            self.rotation_angle += self.rotation_speed
    
    def render_menu(self):
        """Renderiza la pantalla de menú"""
        self.screen.fill((10, 10, 20))
        UIRenderer.draw_menu_screen(self.screen)
        
        for button in self.menu_buttons:
            button.draw(self.screen)
    
    def render_viewer(self):
        """Renderiza el visualizador 3D"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.05, 0.05, 0.1, 1.0)
        
        glUseProgram(self.shader_program)
        self.renderer.setup_uniforms()
        glBindVertexArray(self.sphere.vao)
        
        # Renderizar esferas según el modo
        if self.view_mode == 0:  # Todas
            self.renderer.render_sphere(self.materials['metal'], [-3.5, 0.0, 0.0], self.rotation_angle)
            self.renderer.render_sphere(self.materials['water'], [0.0, 0.0, 0.0], self.rotation_angle)
            self.renderer.render_sphere(self.materials['matte'], [3.5, 0.0, 0.0], self.rotation_angle)
        elif self.view_mode == 1:  # Metal
            self.renderer.render_sphere(self.materials['metal'], [0.0, 0.0, 0.0], self.rotation_angle)
        elif self.view_mode == 2:  # Agua
            self.renderer.render_sphere(self.materials['water'], [0.0, 0.0, 0.0], self.rotation_angle)
        elif self.view_mode == 3:  # Opaco
            self.renderer.render_sphere(self.materials['matte'], [0.0, 0.0, 0.0], self.rotation_angle)
        
        # Convertir OpenGL a superficie pygame
        glReadBuffer(GL_BACK)
        pixels = glReadPixels(0, 0, self.display[0], self.display[1], GL_RGB, GL_UNSIGNED_BYTE)
        gl_surface = pygame.image.fromstring(pixels, self.display, "RGB")
        gl_surface = pygame.transform.flip(gl_surface, False, True)
        
        self.screen.blit(gl_surface, (0, 0))
        
        # Dibujar UI
        self.ui_surface.fill((0, 0, 0, 0))
        UIRenderer.draw_viewer_ui(self.ui_surface, self.view_mode, self.rotation_speed, 
                                   self.paused, self.viewer_buttons)
        self.screen.blit(self.ui_surface, (0, 0))
    
    def render(self):
        """Renderiza la escena actual"""
        if self.in_menu:
            self.render_menu()
        else:
            self.render_viewer()
        
        pygame.display.flip()
    
    def run(self):
        """Bucle principal de la aplicación"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()



def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()