import unittest
import unittest.mock

from Main.graphicobjects import GraphicObject
from Main.geometrytransformation2d import Vector2D
from Main.engines import World, CollisionHandler

# -----------------------------------------------------------------


class CollisionHandlerTest(unittest.TestCase):
    @unittest.mock.patch('pygame.Surface')
    @unittest.mock.patch('Main.graphicobjects.GraphicObject.collision_handler')
    def test_handle_with_three_object_that_collide_should_call_the_correct_collision_handler_on_the_objects(self, mock_collision_handler, mock_pygame_surface):
        object_1 = GraphicObject (0, 0, [Vector2D(10, 10), Vector2D(10, -10), Vector2D(-10, -10), Vector2D(-10, 10)])
        object_2 = GraphicObject (10, 10, [Vector2D(10, 10), Vector2D(10, -10), Vector2D(-10, -10), Vector2D(-10, 10)])
        object_3 = GraphicObject (0, 10, [Vector2D(10, 10), Vector2D(10, -10), Vector2D(-10, -10), Vector2D(-10, 10)])

        world = World((100, 100))
        world.add_object(object_1)
        world.add_object(object_2)
        world.add_object(object_3)

        collision_handler = CollisionHandler(world)
        collision_handler.handle()

        calls_counter = mock_collision_handler.call_count

        raise Exception('not implemented')

    def test_handle_with_three_object_and_two_of_them_that_collide_should_call_the_correct_collision_handler_on_the_objects(self):
        raise Exception('not implemented')

    def test_handle_with_no_objects_that_collide_should_not_call_the_collision_handler_on_the_objects(self):
        raise Exception('not implemented')