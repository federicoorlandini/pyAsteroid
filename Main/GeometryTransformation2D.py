""" This class is a 2D vector """


class Vector2D(object):
    x = 0
    y = 0
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, vector):
        return Vector2D(self.x + vector.x, self.y + vector.y)

""" this class contains helper methods to execute some 2D transformations """


class GeometryTransformation2D(object):
    def __init__(self, lookup_table):
        self.lookup_table = lookup_table
        
    def rotate(self, vertex, angle):
        if angle < 0:
            sin_sign = -1
        else:
            sin_sign = 1
        
        angle = abs(angle)
        
        new_x = vertex.x * self.lookup_table.cos[angle] - sin_sign * vertex.y * self.lookup_table.sin[angle]
        new_y = sin_sign * vertex.x * self.lookup_table.sin[angle] + vertex.y * self.lookup_table.cos[angle]
        
        vertex.x = new_x
        vertex.y = new_y
        
    def move_in_a_direction(self, vertex, angle_in_degree, length):
        new_x = vertex.x + self.lookup_table.cos[angle_in_degree] * length
        new_y = vertex.y - self.lookup_table.sin[angle_in_degree] * length
        return Vector2D(new_x, new_y)