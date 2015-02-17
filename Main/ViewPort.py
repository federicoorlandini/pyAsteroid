'''
Created on 07/dic/2014

@author: Federico
'''
from Main.Geometry2D import Point2D
import pygame

class ViewPort(object):
    '''
    classdocs
    '''
    width = 0
    height = 0
    
    draw_surface = None
    
    def __init__(self, width = 0, height = 0, draw_surface = None):
        self.width = width
        self.height = height
        self.draw_surface = draw_surface
        
    def ToScreenCoordinate(self, x, y):
        viewportX = self.width / 2 + x
        viewportY = self.height / 2 +y
        return Point2D(viewportX, viewportY)  
    
    def draw_vertexes(self, position_x, position_y, vertex_list, color):
        points = []
        for v in vertex_list:
            p =  self.ToScreenCoordinate(v.x + position_x, v.y + position_y)
            points.append((p.x, p.y))
        pygame.draw.lines(self.draw_surface, color, True, points, 1 )