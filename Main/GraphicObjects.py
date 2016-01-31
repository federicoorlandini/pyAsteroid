'''
Created on 13/mag/2014

@author: Federico
'''
import pygame
import Main.Constants
from Main.Geometry2D import Vector2D, Geometry2D

''' GraphicObject: the base class for every object on the screen '''


class GraphicObject(object):
    _geometry2D = Geometry2D(Main.Constants.LOOKUP_TABLE)
    position = Vector2D()
    _angle = 0
    _color = Main.Constants.WHITE;
    _vertexes = None
    _lookupTable = object()

    def __init__(self, x=0, y=0, color=Main.Constants.WHITE, lookup_table=Main.Constants.LOOKUP_TABLE, vertexes=None):
        self.position.x = x
        self.position.y = y
        self._color = color
        self._lookupTable = lookup_table
        self._vertexes = vertexes
        self.angle = 0

    def move(self, angle, length):
        self.position = self._geometry2D.move(self.position, angle, length)

    def rotate(self, relative_angle):
        self.angle = int((self.angle + relative_angle) % 360)
        new_vertexes = []
        absolute_angle = abs(relative_angle)

        # In a normal axis coordinates system ( Y to the up ),
        # these values should be inverted (angle > 0 => +1, angle < 0 => -1)
        # but we consider a coordinate system where the Y axis goes down
        if relative_angle < 0:
            sin_sign = 1
        else:
            sin_sign = -1

        for vertex in self._vertexes:
            new_vertex = Vector2D()
            new_vertex.x = vertex.x * self._lookupTable.cos[absolute_angle] - sin_sign * vertex.y * \
                                                                              self._lookupTable.sin[absolute_angle]
            new_vertex.y = sin_sign * vertex.x * self._lookupTable.sin[absolute_angle] + vertex.y * \
                                                                                         self._lookupTable.cos[
                                                                                             absolute_angle]
            new_vertexes.append(new_vertex)
        self._vertexes = tuple(new_vertexes)

    def update_position(self):
        pass  # Nothing to do here

    def draw(self, viewport):
        viewport.draw_vertexes(self.position.x, self.position.y, self._vertexes, self._color)


''' Class STARSHIP '''


class StarShip(GraphicObject):
    def __init__(self, x, y, color, lookup_table):
        super().__init__()
        self._vertexes = (Vector2D(20, 0),
                          Vector2D(-10, -10),
                          Vector2D(0, 0),
                          Vector2D(-10, 10))

    def fire(self):
        return Bullet(self.angle)


''' This is a single bullet that is fired from the Star ship '''


class Bullet(GraphicObject):
    angle = 0  # Direction of movement (angle)
    speed = 10  # speed movement (in pixel per call)

    def __init__(self, angle_of_direction):
        self.angle = angle_of_direction
        self._vertexes = (Vector2D(-3,0), Vector2D(3, 0))

    def update_position(self):
        self.move(self.angle, self.speed)
