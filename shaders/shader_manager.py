import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math


class ShaderManager:
    """Gestiona la compilación y creación de shaders"""
    
    VERTEX_SHADER = """
    #version 330 core
    layout(location = 0) in vec3 position;
    layout(location = 1) in vec3 normal;
    layout(location = 2) in vec2 texCoord;

    out vec3 FragPos;
    out vec3 Normal;
    out vec2 TexCoord;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main()
    {
        FragPos = vec3(model * vec4(position, 1.0));
        Normal = mat3(transpose(inverse(model))) * normal;
        TexCoord = texCoord;
        gl_Position = projection * view * vec4(FragPos, 1.0);
    }
    """

    FRAGMENT_SHADER = """
    #version 330 core
    in vec3 FragPos;
    in vec3 Normal;
    in vec2 TexCoord;

    out vec4 FragColor;

    uniform vec3 lightPos;
    uniform vec3 viewPos;
    uniform vec3 lightColor;

    uniform vec3 materialAmbient;
    uniform vec3 materialDiffuse;
    uniform vec3 materialSpecular;
    uniform float materialShininess;
    uniform float materialReflectivity;
    uniform int materialType;

    void main()
    {
        vec3 norm = normalize(Normal);
        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 lightDir = normalize(lightPos - FragPos);
        
        vec3 ambient = materialAmbient * lightColor;
        
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = diff * materialDiffuse * lightColor;
        
        vec3 reflectDir = reflect(-lightDir, norm);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), materialShininess);
        vec3 specular = spec * materialSpecular * lightColor;
        
        vec3 textureColor = materialDiffuse;
        
        if (materialType == 0) {
            float noise = fract(sin(dot(TexCoord, vec2(12.9898, 78.233))) * 43758.5453);
            float variation = mix(0.95, 1.0, noise);
            textureColor = materialDiffuse * variation;
            specular *= 1.3;
        }
        else if (materialType == 1) {
            float wave1 = sin(TexCoord.x * 8.0 + TexCoord.y * 5.0) * 0.5 + 0.5;
            float wave2 = cos(TexCoord.x * 6.0 - TexCoord.y * 4.0) * 0.5 + 0.5;
            float wave3 = sin(TexCoord.x * 10.0 + TexCoord.y * 7.0) * 0.5 + 0.5;
            
            float waves = (wave1 * 0.4 + wave2 * 0.35 + wave3 * 0.25);
            textureColor = mix(materialDiffuse * 0.92, materialDiffuse * 1.08, waves);
            
            float caustics = pow(sin(TexCoord.x * 20.0) * sin(TexCoord.y * 20.0) * 0.5 + 0.5, 2.0) * 0.1;
            specular += vec3(caustics);
        }
        else if (materialType == 2) {
            float grain1 = fract(sin(dot(TexCoord, vec2(12.9898, 78.233))) * 43758.5453);
            float grain2 = fract(sin(dot(TexCoord * 2.0, vec2(39.346, 11.135))) * 73156.8473);
            float grain = (grain1 + grain2) * 0.5;
            textureColor = materialDiffuse * mix(0.9, 1.0, grain);
            specular *= 0.3;
        }
        
        vec3 reflectionComponent = vec3(0.0);
        if (materialReflectivity > 0.3) {
            vec3 reflection = reflect(-viewDir, norm);
            float fresnel = pow(1.0 - max(dot(viewDir, norm), 0.0), 1.5);
            vec3 reflectionColor = vec3(0.3, 0.4, 0.5);
            reflectionComponent = materialReflectivity * reflectionColor * fresnel * 0.3;
        }
        
        diffuse *= textureColor;
        vec3 result = ambient + diffuse + specular + reflectionComponent;
        FragColor = vec4(result, 1.0);
    }
    """
    
    @staticmethod
    def compile_shader(source, shader_type):
        """Compila un shader individual"""
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(shader).decode()
            raise RuntimeError(f"Shader compilation failed: {error}")
        
        return shader
    
    @staticmethod
    def create_program():
        """Crea el programa de shaders completo"""
        vertex = ShaderManager.compile_shader(ShaderManager.VERTEX_SHADER, GL_VERTEX_SHADER)
        fragment = ShaderManager.compile_shader(ShaderManager.FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        
        program = glCreateProgram()
        glAttachShader(program, vertex)
        glAttachShader(program, fragment)
        glLinkProgram(program)
        
        if not glGetProgramiv(program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(program).decode()
            raise RuntimeError(f"Program linking failed: {error}")
        
        glDeleteShader(vertex)
        glDeleteShader(fragment)
        
        return program
