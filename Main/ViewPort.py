'''
Created on 07/dic/2014

@author: Federico
'''
from Main.GeometryTransformation2D import Vector2D
import pygame

class ViewPort(object):
    width = 0
    height = 0
    
    draw_surface = None
    
    def __init__(self, width=0, height=0, draw_surface=None):
        self.width = width
        self.height = height
        self.draw_surface = draw_surface
        
    def to_screen_coordinate(self, x, y):
        viewport_x = self.width / 2 + x
        viewport_y = self.height / 2 + y
        return Vector2D(viewport_x, viewport_y)
    
    def draw_vertexes(self, position_x, position_y, vertex_list, color):
        points = []
        for v in vertex_list:
            p = self.to_screen_coordinate(v.x + position_x, v.y + position_y)
            points.append((p.x, p.y))
        pygame.draw.lines(self.draw_surface, color, True, points, 1)