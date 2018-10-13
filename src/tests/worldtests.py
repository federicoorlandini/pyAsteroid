import unittest
import unittest.mock
import engines
from graphicobjects import GraphicObject
from engines import World
from geometrytransformation2d import Vector2D

# -----------------------------------------------------------------


class WorldTest(unittest.TestCase):
    def add_object_shouldAddTheObjectToTheList(self):
        world = engines.World()
        obj = GraphicObject()

        world.add_object(obj)

        self.assertEqual(len(world._objects_list), 1)

    def test_is_object_visible_anObjectVeryFarFromTheViewportCenter_shoudlBeNotVisible(self):
        # We have an object that is outside the viewport
        graph_object = GraphicObject(x=10000, y=10000, vertexes_local=(Vector2D(0, 0), Vector2D(10, 10)))
        world = World((100, 100))
        is_visible = world._is_object_visible(graph_object)
        self.assertFalse(is_visible, "the object should be not visible")

    def test_is_object_visible_anObjectInTheCenterOfTheViewportCenter_shoudlBeVisible(self):
        # We have an object that is in the center or the screen
        graph_object = GraphicObject(x=0, y=0, vertexes_local=(Vector2D(0, 0), Vector2D(10, 10)))

        width = 600
        height = 400
        world = World((width, height))
        # TODO - Should test on the GrahpicObject, not on viewPort
        is_visible = world._is_object_visible(graph_object)
        self.assertTrue(is_visible, "the object should be visible")

    @unittest.mock.patch('engines.CollisionHandler.handle')
    @unittest.mock.patch('pygame.Surface')
    def test_process_should_call_detect_collision(self, surface_mock, mock):
        world = World((100, 100))
        world.process(1)
        self.assertTrue(mock.called)