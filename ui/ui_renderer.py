import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

class UIRenderer:
    """Renderiza los elementos de la interfaz de usuario"""
    
    @staticmethod
    def draw_menu_screen(surface):
        """Dibuja la pantalla del menú principal"""
        surface.fill((10, 10, 20))
        
        font_title = pygame.font.Font(None, 72)
        title = font_title.render("PRÁCTICA CALIFICADA 2", True, (100, 200, 255))
        title_rect = title.get_rect(center=(600, 150))
        surface.blit(title, title_rect)
        
        font_subtitle = pygame.font.Font(None, 36)
        subtitle = font_subtitle.render("Renderizado de Esferas con Diferentes Materiales", True, (150, 150, 200))
        subtitle_rect = subtitle.get_rect(center=(600, 220))
        surface.blit(subtitle, subtitle_rect)
        
        pygame.draw.line(surface, (100, 200, 255), (200, 260), (1000, 260), 3)
        
        font_info = pygame.font.Font(None, 28)
        info_texts = [
            "Computación Gráfica",
            "Shaders GLSL - Iluminación Phong",
            "Lautaro Quispe Ballesteros - 20210206I",
        ]
        
        y_pos = 320
        for text in info_texts:
            info_surf = font_info.render(text, True, (200, 200, 220))
            info_rect = info_surf.get_rect(center=(600, y_pos))
            surface.blit(info_surf, info_rect)
            y_pos += 40
    
    @staticmethod
    def draw_viewer_ui(surface, view_mode, rotation_speed, paused, buttons):
        """Dibuja la interfaz del visualizador 3D"""
        # Panel superior
        panel_top = pygame.Surface((1200, 80))
        panel_top.set_alpha(230)
        panel_top.fill((15, 15, 25))
        surface.blit(panel_top, (0, 0))
        
        font_title = pygame.font.Font(None, 42)
        title = font_title.render("PRÁCTICA CALIFICADA 2 - Viewer 3D", True, (100, 200, 255))
        surface.blit(title, (20, 15))
        
        font_controls = pygame.font.Font(None, 20)
        controls_text = "[ESPACIO] Pausa  |  [+/-] Velocidad  |  [R] Reset  |  [M] Menú  |  [ESC] Salir"
        controls_surf = font_controls.render(controls_text, True, (180, 180, 180))
        surface.blit(controls_surf, (20, 55))
        
        # Panel lateral
        panel_side = pygame.Surface((280, 350))
        panel_side.set_alpha(220)
        panel_side.fill((20, 20, 35))
        surface.blit(panel_side, (910, 100))
        
        font_section = pygame.font.Font(None, 28)
        font_text = pygame.font.Font(None, 22)
        
        y = 115
        section = font_section.render("INFORMACIÓN", True, (100, 200, 255))
        surface.blit(section, (930, y))
        
        y += 50
        mode_names = {
            0: "Todas las Esferas",
            1: "Esfera Metálica",
            2: "Esfera de Agua",
            3: "Esfera Opaca"
        }
        
        mode_text = font_text.render("Modo Actual:", True, (180, 180, 180))
        surface.blit(mode_text, (930, y))
        y += 25
        mode_value = font_text.render(mode_names[view_mode], True, (100, 255, 100))
        surface.blit(mode_value, (945, y))
        
        y += 45
        speed_text = font_text.render("Velocidad:", True, (180, 180, 180))
        surface.blit(speed_text, (930, y))
        y += 25
        speed_value = font_text.render(f"{rotation_speed:.1f}x", True, (255, 200, 100))
        surface.blit(speed_value, (945, y))
        
        y += 45
        status_text = font_text.render("Estado:", True, (180, 180, 180))
        surface.blit(status_text, (930, y))
        y += 25
        status = "PAUSADO" if paused else "ACTIVO"
        status_color = (255, 100, 100) if paused else (100, 255, 100)
        status_value = font_text.render(status, True, status_color)
        surface.blit(status_value, (945, y))
        
        y = 470
        section_btn = font_section.render("SELECCIÓN", True, (100, 200, 255))
        surface.blit(section_btn, (930, y))
        
        for i, button in enumerate(buttons):
            button.draw(surface, is_active=(i == view_mode))