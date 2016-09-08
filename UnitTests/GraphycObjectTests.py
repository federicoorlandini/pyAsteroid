import unittest
import unittest.mock

import math
from Main import values
from Main import constants
from Main import lookuptables
from Main.graphicobjects import GraphicObject
from Main.graphicobjects import StarShip
from Main.geometrytransformation2d import Vector2D
from Main.engines import World


# -----------------------------------------------------------------------
class GraphicObjectTests(unittest.TestCase):
    def test_move_shouldChangeThePositionOfTheObjectInTheCorrectWay(self):
        # fake world
        world = World((100, 100))
        obj = GraphicObject(world)
        movement_angle = 45
        movement_length = 10

        expected_x = 10 / math.sqrt(2)
        expected_y = expected_x

        obj._move(movement_angle, movement_length)

        self.assertTrue(values.are_equals(obj.position.x, expected_x), "The X coordinate is wrong")
        self.assertTrue(values.are_equals(obj.position.y, expected_y), "The y coordinate is wrong")

    def test_rotate_shoudUpdateTheHeadAngleOfTheObject(self):
        # fake world
        world = World((100, 100))
        obj = GraphicObject(world, vertexes_local=(Vector2D(1, 0),))
        rotation_angle = 45

        obj.rotate_head_direction(rotation_angle)

        self.assertEqual(obj.head_angle, rotation_angle)

    def test_get_collision_circle(self):
        # fake world
        world = World((100, 100))
        # Prepare the object with vertexes like a square with the center in (0, 0) and
        # width and height 10 pixels
        object_vertexes = (Vector2D(5, 5), Vector2D(5, -5), Vector2D(-5, -5), Vector2D(-5, 5))
        graph_object = GraphicObject(world, x=0, y=0, vertexes_local=object_vertexes)
        graph_object._compute_collision_circle()
        # The expected radius is the following
        expected_radius = 5 * math.sqrt(2)
        # Assert
        self.assertTrue(values.are_equals(graph_object.collision_circle.radius, expected_radius))

    @unittest.mock.patch('Main.graphicobjects.GraphicObject._compute_collision_circle')
    def test_process_should_update_the_collision_circle(self, mock):
        # fake world
        world = World((100, 100))
        # Prepare the object with vertexes like a square with the center in (0, 0) and
        # width and height 10 pixels
        object_vertexes = (Vector2D(5, 5), Vector2D(5, -5), Vector2D(-5, -5), Vector2D(-5, 5))
        graph_object = GraphicObject(world, x=0, y=0, vertexes_local=object_vertexes)
        graph_object.process(1)
        self.assertTrue(mock.called)


# -----------------------------------------------------------------------
class StarShipTests(unittest.TestCase):
    # fake world
    _world = World((100, 100))
    _lookup_table = lookuptables.CosSinTable()

    def test_fire_withReloadCounterNotZero_shouldNotFireABullet(self):
        ship = StarShip(self._world, 0, 0, constants.WHITE, self._lookup_table)
        ship.reload_counter = 1
        bullet = ship.fire()
        self.assertIsNone(bullet)

    def test_fire_withReloadCounterZero_shouldFireABullet(self):
        ship = StarShip(self._world, 0, 0, constants.WHITE, self._lookup_table)
        ship.reload_counter = 0
        bullet = ship.fire()
        self.assertIsNotNone(bullet)

    def test_fire_withReloadCounterZero_shouldResetTheReloadCounter(self):
        ship = StarShip(self._world, 0, 0, constants.WHITE, self._lookup_table)
        ship.reload_counter = 0
        ship.fire()
        self.assertNotEqual(ship.reload_counter, 0)


# -----------------------------------------------------------------------
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
