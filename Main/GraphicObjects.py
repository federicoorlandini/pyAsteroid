import Main.constants
from Main.geometrytransformation2d import Vector2D, GeometryTransformation2D

# -----------------------------------------------------------------


class GraphicObject(object):
    """ GraphicObject: the base class for every object on the screen """
    _geometry2D = GeometryTransformation2D(Main.constants.LOOKUP_TABLE)
    _color = Main.constants.WHITE

    def __init__(self, x=0, y=0, color=Main.constants.WHITE, lookup_table=Main.constants.LOOKUP_TABLE, vertexes_local=None):
        self.position = Vector2D(x, y)
        self._color = color
        self._lookupTable = lookup_table
        self.object_vertexes = vertexes_local   # These are the vertex that are relative to the object coordinates
        self.head_angle = 0 # This is the angle that determine the direction of the object
        self.rotation_angle = 0  # This is the angle of rotation of the object on its center point
        self.speed = 0  # The movement speed in pixel/sec

    """ This method move the Graphical object """
    def _move(self, angle, length):
        self.position = self._geometry2D.move_in_a_direction(self.position, angle, length)

    """ This method rotate the head direction of the Graphical object """
    def rotate_head_direction(self, relative_angle):
        self.head_angle = int((self.head_angle + relative_angle) % 360)

    """ This method rotate the Graphical object around its position point """
    def rotate_object(self, relative_angle):
        self.rotation_angle = int((self.rotation_angle + relative_angle) % 360)

    def process(self, delta_time):
        # Must move the object in the heading direction based on the speed
        distance = self.speed * delta_time
        self._move(self.head_angle, distance)

    def _get_world_coordinate(self, world_vertex):
        # Build the vertex coordinate relative to the world axis (where (0,0) is the center of the screen)
        rotated_vertex = self._geometry2D.rotate(world_vertex, self.head_angle)
        world_vertex = self._geometry2D.translate(rotated_vertex, self.position.x, self.position.y)
        return world_vertex

    def get_world_vertexes(self):
        return [self._get_world_coordinate(v) for v in self.object_vertexes]

    def render(self, viewport):
        # For each vertex, we must rotate it and translate it
        world_vertexes = self.get_world_vertexes();
        viewport.draw_world_vertexes(world_vertexes, self._color)

# -----------------------------------------------------------------


class StarShip(GraphicObject):
    """ Class STAR SHIP """
    RELOAD_COUNTER_DEFAULT_VALUE = 10

    def __init__(self, x, y, color, lookup_table):
        super().__init__(x, y, color, lookup_table)
        self.object_vertexes = (Vector2D(20, 0),
                                Vector2D(-10, -10),
                                Vector2D(0, 0),
                                Vector2D(-10, 10))
        self.reload_counter = self.RELOAD_COUNTER_DEFAULT_VALUE

    def fire(self):
        if not self.is_reloading():
            start_position = self._get_world_coordinate(self.object_vertexes[0])
            bullet = Bullet(start_position.x, start_position.y, self.head_angle)
            self._reset_reload_counter()
            return bullet

    def process(self, delta_time):
        self._update_reload_counter()
        super().process(delta_time)

    def is_reloading(self):
        return self.reload_counter > 0

    def _update_reload_counter(self):
        if self.is_reloading():
            self.reload_counter -= 1

    def _reset_reload_counter(self):
        self.reload_counter = self.RELOAD_COUNTER_DEFAULT_VALUE
# -----------------------------------------------------------------


class Bullet(GraphicObject):
    """ This is a single bullet that is fired from the Star ship """

    def __init__(self, x, y, angle_of_direction, speed=150):
        super().__init__(x, y)
        self.head_angle = angle_of_direction
        self.speed = speed
        self.object_vertexes = (Vector2D(-3, 0), Vector2D(3, 0))


# -----------------------------------------------------------------


class Asteroid(GraphicObject):
    def __init__(self, x, y, angle_of_direction, speed):
        super(Asteroid, self).__init__(x, y)
        self.head_angle = angle_of_direction
        self.speed = speed
        self.object_vertexes = (Vector2D(10, 10), Vector2D(-10, 10), Vector2D(-10, -10), Vector2D(10, -10))  # A rectangle
