import Main.Constants
from Main.GeometryTransformation2D import Vector2D, GeometryTransformation2D

# -----------------------------------------------------------------


class GraphicObject(object):
    """ GraphicObject: the base class for every object on the screen """
    _geometry2D = GeometryTransformation2D(Main.Constants.LOOKUP_TABLE)
    _angle = 0
    _color = Main.Constants.WHITE
    _vertexes_local = None    # These are the vertex that are relative to the object coordinates
    _lookupTable = object()

    def __init__(self, x=0, y=0, color=Main.Constants.WHITE, lookup_table=Main.Constants.LOOKUP_TABLE, vertexes_local=None):
        self.position = Vector2D(x, y)
        self._color = color
        self._lookupTable = lookup_table
        self._vertexes_local = vertexes_local
        self.angle = 0

    """ This method move the Graphical object """
    def move(self, angle, length):
        self.position = self._geometry2D.move_in_a_direction(self.position, angle, length)

    """ This method rotate the Graphical object """
    def rotate(self, relative_angle):
        self.angle = int((self.angle + relative_angle) % 360)

    def update_position(self):
        pass  # Nothing to do here

    def _get_absolute_coordinate(self, vertex):
        rotated_vertex = self._geometry2D.rotate(vertex, self.angle)
        absolute_vertex = self._geometry2D.translate(rotated_vertex, self.position.x, self.position.y)
        return absolute_vertex

    def draw(self, viewport):
        # For each vertex, we must rotate it and translate it
        vertexes = [self._get_absolute_coordinate(v) for v in self._vertexes_local]
        viewport.draw_vertexes(vertexes, self._color)

# -----------------------------------------------------------------


class StarShip(GraphicObject):
    """ Class STAR SHIP """
    def __init__(self, x, y, color, lookup_table):
        super().__init__(x, y, color, lookup_table)
        self._vertexes_local = (Vector2D(20, 0),
                                Vector2D(-10, -10),
                                Vector2D(0, 0),
                                Vector2D(-10, 10))

    def fire(self):
        start_position = self._get_absolute_coordinate(self._vertexes_local[0])
        bullet = Bullet(start_position.x, start_position.y, self.angle)
        return bullet

# -----------------------------------------------------------------


class Bullet(GraphicObject):
    """ This is a single bullet that is fired from the Star ship """
    angle = 0  # Direction of movement (angle)
    speed = 10  # speed movement (in pixel per call)

    def __init__(self, x, y, angle_of_direction):
        super().__init__(x, y)
        self.position.x = x
        self.position.y = y
        self.angle = angle_of_direction
        self._vertexes_local = (Vector2D(-3, 0), Vector2D(3, 0))

    def update_position(self):
        self.move(self.angle, self.speed)
