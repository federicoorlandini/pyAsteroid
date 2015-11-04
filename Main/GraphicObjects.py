'''
Created on 13/mag/2014

@author: Federico
'''
import pygame
import Main.Constants
from Main.Geometry2D import Point2D, Geometry2D

''' GraphicObject: the base class for every object on the screen '''     
class GraphicObject(object):
    _geometry2D = Geometry2D(Main.Constants.LOOKUP_TABLE)
    position = Point2D()
    _angle = 0
    _color = Main.Constants.WHITE;
    _vertexes = None
    _lookupTable = object()
    
    def __init__(self, x = 0, y = 0, color = Main.Constants.WHITE, lookupTable = Main.Constants.LOOKUP_TABLE, vertexes = None):
        self.position.x = x
        self.position.y = y
        self._color = color
        self._lookupTable = lookupTable
        self._vertexes = vertexes
        self.angle = 0
        
    def move(self, angle, length):
        self.position = self._geometry2D.move(self.position, angle, length)
    
    def rotate(self, angleRelative):
        self.angle = int((self.angle + angleRelative) % 360)
        newVertexes = []
        angleAbsolute = abs(angleRelative)
        
        # In a normal axis coordinates system ( Y to the up ), these values should be inverted (angle > 0 => +1, angle < 0 => -1)
        # but we consider a coordinate system where the Y axis goes down
        if(angleRelative < 0):
            sinSign = 1
        else:
            sinSign = -1
            
        for vertex in self._vertexes:
            newVertex = Point2D()
            newVertex.x = vertex.x * self._lookupTable.cos[angleAbsolute] - sinSign * vertex.y * self._lookupTable.sin[angleAbsolute]
            newVertex.y = sinSign * vertex.x * self._lookupTable.sin[angleAbsolute] + vertex.y * self._lookupTable.cos[angleAbsolute]
            newVertexes.append(newVertex)
        self._vertexes = tuple(newVertexes)
    
    def update_position(self):
        pass;   # Nothing to do here
             
    def draw(self, viewport):
        viewport.draw_vertexes(self.position.x, self.position.y, self._vertexes, self._color)
        
    
''' Class STARSHIP '''
class StarShip(GraphicObject):
    def __init__(self, x, y, color, lookup_table):
        super().__init__()
        _vertexes = (Point2D(0, 20), 
               Point2D(-10, -10), 
               Point2D(0, 0), 
               Point2D(10, -10))
    
        
''' This is a single bullet that is fired from the Starship '''
class Bullet(GraphicObject):
    moveDirection = 0   # Direction of movement (angle)
    speed = 0           # speed movement (in pixel per call)
    
    def update_position(self):
        self.move(self.moveDirection, self.speed)
    
    def draw(self, drawsurface):
        pygame.draw.line(drawsurface, self.color, self.position, self.position, width=1)