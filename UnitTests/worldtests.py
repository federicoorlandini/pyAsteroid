import unittest
import unittest.mock
import Main.engines



class WorldTest(unittest.TestCase):
    def add_object_shouldAddTheObjectToTheList(self):
        world = Main.engines.World()
        obj = Main.graphicobjects.GraphicObject()

        world.add_object(obj)

        self.assertEqual(len(world.object_list), 1)

    @unittest.mock.patch('Main.engines.World.detect_collision')
    @unittest.mock.patch('pygame.Surface')
    def test_process_should_call_detect_collision(self, surface_mock, mock):
        world = Main.engines.World((100, 100))
        world.process(1)
        self.assertTrue(mock.called)