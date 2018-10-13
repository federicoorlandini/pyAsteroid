from geometrytransformation2d import Vector2D
import pygame


# -----------------------------------------------------------------------
class Display(object):
    def __init__(self, width=0, height=0, draw_surface=None):
        self.width = width
        self.height = height
        self.draw_surface = draw_surface
        
    def _to_display_coordinate(self, world_vertex):
        display_x = self.width / 2 + world_vertex.x
        display_y = self.height / 2 + world_vertex.y
        return Vector2D(display_x, display_y)
    
    def draw_world_vertexes(self, world_vertex_list, color):
        points = []
        for vertex in world_vertex_list:
            p = self._to_display_coordinate(vertex)
            points.append((p.x, p.y))
        pygame.draw.lines(self.draw_surface, color, True, points, 1)
