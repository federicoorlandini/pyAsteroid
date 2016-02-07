class Vector2D(object):
    x = 0
    y = 0
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, vector):
        return Vector2D(self.x + vector.x, self.y + vector.y)


class GeometryTransformation2D(object):
    """ this class contains helper methods to execute some 2D transformations """
    def __init__(self, lookup_table):
        self.lookup_table = lookup_table
        
    def rotate(self, vertex, angle):
        """
        if angle < 0:
            sin_sign = -1
        else:
            sin_sign = 1
        
        angle = abs(angle)
        
        x = vertex.x * self.lookup_table.cos[angle] - sin_sign * vertex.y * self.lookup_table.sin[angle]
        y = sin_sign * vertex.x * self.lookup_table.sin[angle] + vertex.y * self.lookup_table.cos[angle]
        """

        x = vertex.x * self.lookup_table.cos[angle] - vertex.y * self.lookup_table.sin[angle]
        y = vertex.x * self.lookup_table.sin[angle] + vertex.y * self.lookup_table.cos[angle]

        return Vector2D(x, y)
        
    def move_in_a_direction(self, vertex, angle_in_degree, length):
        """ Move the vertex in the specific direction for a specific length
        :param vertex: the vertex to move
        :param angle_in_degree: the angle where move the vertex
        :param length: the movement length
        :return: a vertex that represent the new position
        """
        new_x = vertex.x + self.lookup_table.cos[angle_in_degree] * length
        new_y = vertex.y + self.lookup_table.sin[angle_in_degree] * length
        return Vector2D(new_x, new_y)

    def translate(self, vertex, x, y):
        """ Translate the vertex
        :param vertex: the vertex to translate
        :param x: the variation on the X axis
        :param y: the variation on the Y axis
        :return: a vertex that represent the new position
        """
        new_x = vertex.x + x
        new_y = vertex.y + y
        return Vector2D(new_x, new_y)