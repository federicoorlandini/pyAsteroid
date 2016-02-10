import Main.Constants
from Main.GeometryTransformation2D import Vector2D, GeometryTransformation2D

# -----------------------------------------------------------------


class GraphicObject(object):
    """ GraphicObject: the base class for every object on the screen """
    _geometry2D = GeometryTransformation2D(Main.Constants.LOOKUP_TABLE)
    _color = Main.Constants.WHITE

    def __init__(self, x=0, y=0, color=Main.Constants.WHITE, lookup_table=Main.Constants.LOOKUP_TABLE, vertexes_local=None):
        self.position = Vector2D(x, y)
        self._color = color
        self._lookupTable = lookup_table
        self.object_vertexes = vertexes_local   # These are the vertex that are relative to the object coordinates
        self.head_angle = 0 # This is the angle that determine the direction of the object
        self.rotation_angle = 0  # This is the angle of rotation of the object on its center point

    """ This method move the Graphical object """
    def move(self, angle, length):
        self.position = self._geometry2D.move_in_a_direction(self.position, angle, length)

    """ This method rotate the head direction of the Graphical object """
    def rotate_head_direction(self, relative_angle):
        self.head_angle = int((self.head_angle + relative_angle) % 360)

    """ This method rotate the Graphical object around its position point """
    def rotate_object(self, relative_angle):
        self.rotation_angle = int((self.rotation_angle + relative_angle) % 360)

    def update_position(self):
        pass  # Nothing to do here

    def _get_world_coordinate(self, world_vertex):
        # Build the vertex coordinate relative to the world axis (where (0,0) is the center of the screen)
        rotated_vertex = self._geometry2D.rotate(world_vertex, self.head_angle)
        world_vertex = self._geometry2D.translate(rotated_vertex, self.position.x, self.position.y)
        return world_vertex

    def get_world_vertexes(self):
        return [self._get_world_coordinate(v) for v in self.object_vertexes]

    def draw(self, viewport):
        # For each vertex, we must rotate it and translate it
        world_vertexes = self.get_world_vertexes();
        viewport.draw_world_vertexes(world_vertexes, self._color)

# -----------------------------------------------------------------


class StarShip(GraphicObject):
    """ Class STAR SHIP """
    def __init__(self, x, y, color, lookup_table):
        super().__init__(x, y, color, lookup_table)
        self.object_vertexes = (Vector2D(20, 0),
                                Vector2D(-10, -10),
                                Vector2D(0, 0),
                                Vector2D(-10, 10))

    def fire(self):
        start_position = self._get_world_coordinate(self.object_vertexes[0])
        bullet = Bullet(start_position.x, start_position.y, self.head_angle)
        return bullet

# -----------------------------------------------------------------


class Bullet(GraphicObject):
    """ This is a single bullet that is fired from the Star ship """
    head_angle = 0  # Direction of movement (angle)

    def __init__(self, x, y, angle_of_direction, speed=10):
        super().__init__(x, y)
        self.head_angle = angle_of_direction
        self.speed = speed
        self.object_vertexes = (Vector2D(-3, 0), Vector2D(3, 0))

    def update_position(self):
        self.move(self.head_angle, self.speed)

# -----------------------------------------------------------------


class Asteroid(GraphicObject):
    def __init__(self, x, y, angle_of_direction, speed):
        super(Asteroid, self).__init__(x, y)
        self.head_angle = angle_of_direction
        self.speed = speed
        self.object_vertexes = (Vector2D(1, 1), Vector2D(-1, 1), Vector2D(-1, -1), Vector2D(1, -1)) # A rectangle

    def update_position(self):
        self.move(self.head_angle, self.speed)
