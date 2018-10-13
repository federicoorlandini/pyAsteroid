import constants
import math
import geometrytransformation2d
from geometrytransformation2d import Vector2D, Circle

# -----------------------------------------------------------------
class GraphicObject(object):
    """ GraphicObject: the base class for every object on the screen """

    def __init__(self, x=0, y=0, color=constants.WHITE,
                 vertexes_local=None):
        self.position = Vector2D(x, y)
        self.color = color
        self.object_vertexes = vertexes_local  # These are the vertex that are relative to the object coordinates
        self.head_angle = 0  # This is the angle that determine the direction of the object
        self.rotation_angle = 0  # This is the angle of rotation of the object on its center point
        self.speed = 0  # The movement speed in pixel/sec
        self.id = 0 # The unique ID of the object
        self._compute_collision_circle()

    """ This method move the Graphical object """

    def _move(self, angle, length):
        self.position = geometrytransformation2d.move_in_a_direction(self.position, angle, length)

    """ This method compute the circle for the collision detection """

    def _compute_collision_circle(self):
        if self.object_vertexes is None:
            return None

        # Compute the radius getting the max of the distance of each vertex from the origin of the object
        distances = [v.magnitude_power_2() for v in self.object_vertexes]
        radius = math.sqrt(max(distances))
        center = Vector2D(self.position.x, self.position.y)
        self.collision_circle = Circle(center, radius)

    " This method rotate the head direction of the Graphical object "
    def rotate_head_direction(self, relative_angle):
        self.head_angle = int((self.head_angle + relative_angle) % 360)

    " This method rotate the Graphical object around its position point "
    def rotate_object(self, relative_angle):
        self.rotation_angle = int((self.rotation_angle + relative_angle) % 360)

    def process(self, delta_time):
        # Must move the object in the heading direction based on the speed
        distance = self.speed * delta_time
        self._move(self.head_angle, distance)
        self._compute_collision_circle()

    ''' Return the local vertexes of the object '''
    def get_vertexes(self):
        return self.object_vertexes

    def get_color(self):
        return self.color

    def collision_handler(self, collision_info):
        pass

# -----------------------------------------------------------------


class StarShip(GraphicObject):
    """ Class STAR SHIP """
    RELOAD_COUNTER_DEFAULT_VALUE = 10

    def __init__(self, x, y, color):
        object_vertexes = (Vector2D(20, 0),
                           Vector2D(-10, -10),
                           Vector2D(0, 0),
                           Vector2D(-10, 10))
        super().__init__(x, y, color, vertexes_local=object_vertexes)

        self.reload_counter = self.RELOAD_COUNTER_DEFAULT_VALUE

    " This method rotate the StarShip around its position point "
    def rotate_object(self, relative_angle):
        super().rotate_object(relative_angle)
        self.head_angle = int((self.head_angle + relative_angle) % 360)

    def fire(self):
        if not self.is_reloading():
            null_vector = geometrytransformation2d.Vector2D()
            start_position = geometrytransformation2d.from_local_to_world_coordinates(self.object_vertexes[0], null_vector, self.head_angle)
            bullet = Bullet(start_position.x, start_position.y, self.head_angle)
            self._reset_reload_counter()
            return bullet

    def process(self, delta_time):
        self._update_reload_counter()
        super().process(delta_time)

    def is_reloading(self):
        return self.reload_counter > 0

    def collision_handler(self, collision_info, world):
        # Retrieve the type of the other object that collided
        objects_list = world.get_objects_list()
        other_object = objects_list[collision_info.second_collider_object_id]
        if( isinstance(other_object, Bullet) ):
            return
        raise Exception('Not implemented')

    def _update_reload_counter(self):
        if self.is_reloading():
            self.reload_counter -= 1

    def _reset_reload_counter(self):
        self.reload_counter = self.RELOAD_COUNTER_DEFAULT_VALUE


# -----------------------------------------------------------------


class Bullet(GraphicObject):
    """ This is a single bullet that is fired from the Star ship """

    def __init__(self, x, y, angle_of_direction, speed=150):
        object_vertexes = (Vector2D(-3, 0), Vector2D(3, 0))
        super().__init__(x, y ,vertexes_local=object_vertexes)
        self.head_angle = angle_of_direction
        self.speed = speed

    def collision_handler(self, collision_info, world):
        object_list = world.get_objects_list()
        other_object = object_list[collision_info.second_collider_object_id]
        if isinstance(other_object, Asteroid):
            del object_list[collision_info.second_collider_object_id]

# -----------------------------------------------------------------

class Asteroid(GraphicObject):
    def __init__(self, x, y, angle_of_direction, speed):
        object_vertexes = (Vector2D(10, 10), Vector2D(-10, 10), Vector2D(-10, -10), Vector2D(10, -10))  # A rectangle
        super().__init__(x, y, vertexes_local=object_vertexes)
        self.head_angle = angle_of_direction
        self.speed = speed

    def collision_handler(self, collision_info, world):
        self.color = constants.RED
