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
    
    def draw_vertexes(self, vertex_list, color):
        points = []
        for v in vertex_list:
            p = self.to_screen_coordinate(v.x, v.y)
            points.append((p.x, p.y))
        pygame.draw.lines(self.draw_surface, color, True, points, 1)

    def is_object_visible(self, graphic_object):
        for vertex in graphic_object.get:
            screen_coord = self.to_screen_coordinate(vertex.x, vertex.y);
            if screen_coord.x < self.width and screen_coord.x > 0 and screen_coord.y > 0 and screen_coord.y < self.height:
                return True
        # If the code arrive here, it means that there is at least one vertex that is visible
        return False
