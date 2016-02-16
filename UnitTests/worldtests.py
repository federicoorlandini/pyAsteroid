import unittest
import Main


class WorldTest(unittest.TestCase):
    def add_object_shouldAddTheObjectToTheList(self):
        world = Main.engines.World()
        obj = Main.graphicobjects.GraphicObject()

        world.add_object(obj)

        self.assertEqual(len(world.object_list), 1)