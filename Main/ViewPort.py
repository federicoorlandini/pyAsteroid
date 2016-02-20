from Main.geometrytransformation2d import Vector2D
import pygame


class ViewPort(object):
    def __init__(self, width=0, height=0, draw_surface=None):
        self.width = width
        self.height = height
        self.draw_surface = draw_surface
        
    def to_screen_coordinate(self, world_vertex):
        viewport_x = self.width / 2 + world_vertex.x
        viewport_y = self.height / 2 + world_vertex.y
        return Vector2D(viewport_x, viewport_y)
    
    def draw_world_vertexes(self, world_vertex_list, color):
        points = []
        for vertex in world_vertex_list:
            p = self.to_screen_coordinate(vertex)
            points.append((p.x, p.y))
        pygame.draw.lines(self.draw_surface, color, True, points, 1)

    def is_object_visible(self, graphic_object):
        world_vertexes = graphic_object.get_world_vertexes()
        for vertex in world_vertexes:
            screen_coord = self.to_screen_coordinate(vertex)
            if screen_coord.x < self.width and screen_coord.x > 0 and screen_coord.y > 0 and screen_coord.y < self.height:
                return True
        # If the code arrive here, it means that there is at least one vertex that is visible
        return False
