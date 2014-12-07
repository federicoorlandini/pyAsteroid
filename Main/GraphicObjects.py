'''
Created on 13/mag/2014

@author: Federico
'''
import pygame
import math
import Main.Constants

class Point2D(object):
    x = 0
    y = 0
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        

''' Classe STARSHIP '''
class StarShip(object):
    vertexs = ((0, 20), (-10, -10), (0, 0), (10, -10))
    
    xPos = 0;
    yPos = 0;
    color = Main.Constants.WHITE;
    
    angle = 0
    
    _lookupTable = object()
    
    def __init__(self, x, y, color, lookupTable):
        self.xPos = x
        self.yPos = y
        self.color = color
        self._lookupTable = lookupTable
    
    def rotate(self, angleRelative):
        self.angle = int((self.angle + angleRelative) % 360)
        newVertexs = []
        for vertex in self.vertexs:
            newVertex = [0,0]
            newVertex[0] = vertex[0] * self._lookupTable.cos[angleRelative] - vertex[1] * self._lookupTable.sin[angleRelative]
            newVertex[1] = vertex[0] * self._lookupTable.sin[angleRelative] + vertex[1] * self._lookupTable.cos[angleRelative]
            newVertexs.append(newVertex)
        self.vertexs = tuple(newVertexs)
                
    def draw(self, drawSurface):
        points = [(v[0] + self.xPos, v[1] + self.yPos) for v in self.vertexs]
        pygame.draw.lines(drawSurface, self.color, True, points, 1 )