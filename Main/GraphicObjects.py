'''
Created on 13/mag/2014

@author: Federico
'''
import pygame
import math
import Main.Constants
from Main.Geometry2D import Vertex2D, Geometry2D

''' GraphicObject: the base class for every object on the screen '''     
class GraphicObject(object):
    _geometry2D = Geometry2D(Main.Constants.LOOKUP_TABLE)
    _position = Vertex2D(0, 0)
    _angle = 0
    _color = Main.Constants.WHITE;
    
    def move(self, angle, length):
        _position = self._geometry2D.move(self._position, angle, length)
    
''' Classe STARSHIP '''
class StarShip(GraphicObject):
    vertexs = ((0, 20), 
               (-10, -10), 
               (0, 0), (10, -10))
    
    _lookupTable = object()
    
    def __init__(self, x, y, color, lookupTable):
        self.position.x = x
        self.position.y = y
        self.color = color
        self._lookupTable = lookupTable
    
    def rotate(self, angleRelative):
        self.angle = int((self.angle + angleRelative) % 360)
        newVertexs = []
        angleAbsolute = abs(angleRelative)
        
        if(angleRelative < 0):
            sinSign = -1
        else:
            sinSign = 1
            
        for vertex in self.vertexs:
            newVertex = [0,0]
            newVertex[0] = vertex[0] * self._lookupTable.cos[angleAbsolute] - sinSign * vertex[1] * self._lookupTable.sin[angleAbsolute]
            newVertex[1] = sinSign * vertex[0] * self._lookupTable.sin[angleAbsolute] + vertex[1] * self._lookupTable.cos[angleAbsolute]
            newVertexs.append(newVertex)
        self.vertexs = tuple(newVertexs)
       
    def updatePosition(self):
        pass;   # Nothing to do here
             
    def draw(self, viewport, drawSurface):
        points = []
        for v in self.vertexs:
            p =  viewport.ToScreenCoordinate(v[0] + self.position.x, v[1] + self.position.y)
            points.append((p.x, p.y))
        pygame.draw.lines(drawSurface, self.color, True, points, 1 )
        
''' This is a single bullet that is fired from the Starship '''
class Bullet(GraphicObject):
    moveDirection = 0   # Direction of movement (angle)
    speed = 0           # speed movement (in pixel per call)
    
    def updatePosition(self):
        self.move(self.moveDirection, self.speed)
    
    def draw(self, drawsurface):
        pygame.draw.line(drawsurface, self.color, self.position, self.position, width=1)