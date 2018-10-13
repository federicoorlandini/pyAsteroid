import lookuptables
import values

class Vector2D(object):
    """ Thi class define a simple vector in the 2D world
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def magnitude_power_2(self):
        """
        :return: The power two of the length of the vector
        """
        return self.x ** 2 + self.y ** 2


# -----------------------------------------------------------------------
class Circle(object):
    """ This class define a circle. It's used for the collision detection
    """

    def __init__(self, center, radius):
        """
        :param center: A Vector2D that define the center of the circle
        :param radius: The radius of the circle
        :return:
        """
        self.center = center
        self.radius = radius

    def is_intersecting_circle(self, other_circle):
        centers_distance_power_2 = (self.center - other_circle.center).magnitude_power_2()
        threshold = (self.radius + other_circle.radius) ** 2
        return (centers_distance_power_2 <= threshold) or values.are_equals(centers_distance_power_2, threshold)

# -----------------------------------------------------------------------
def rotate(vertex, angle):
    x = vertex.x * lookuptables.cos[angle] - vertex.y * lookuptables.sin[angle]
    y = vertex.x * lookuptables.sin[angle] + vertex.y * lookuptables.cos[angle]
    return Vector2D(x, y)


def move_in_a_direction(vertex, angle_in_degree, length):
    """ Move the vertex in the specific direction for a specific length
    :param vertex: the vertex to move
    :param angle_in_degree: the angle where move the vertex
    :param length: the movement length
    :return: a vertex that represent the new position
    """
    new_x = vertex.x + lookuptables.cos[angle_in_degree] * length
    new_y = vertex.y + lookuptables.sin[angle_in_degree] * length
    return Vector2D(new_x, new_y)


def translate(vertex, x, y):
    """ Translate the vertex
    :param vertex: the vertex to translate
    :param x: the variation on the X axis
    :param y: the variation on the Y axis
    :return: a vertex that represent the new position
    """
    new_x = vertex.x + x
    new_y = vertex.y + y
    return Vector2D(new_x, new_y)


def from_local_to_world_coordinates(vertex, translation, rotation_angle):
    # First, rotation of each vertex
    rotated_vertex = rotate(vertex, rotation_angle)
    # Second, vertex translation
    world_vertex = translate(rotated_vertex, translation.x, translation.y)
    return world_vertex
# -----------------------------------------------------------------------
