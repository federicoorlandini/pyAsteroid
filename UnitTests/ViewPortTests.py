import unittest.mock
from Main import ViewPort
from Main.GeometryTransformation2D import Vector2D
import Main.Constants
from Main.GraphicObjects import GraphicObject


class ViewPortTests(unittest.TestCase):
    def test_ToScreenCoordinate_shouldReturnTheCorrectCoordinate(self):
        # center of the viewport
        viewport_center = Vector2D(0,0)
        width = 600
        height = 400
        viewport = Main.ViewPort.ViewPort(width=width, height=height)
        screen_coordinates = viewport.to_screen_coordinate(viewport_center)

        # Should be mapped in the central point of the screen
        self.assertEqual(screen_coordinates.x, 300, "Wrong X coordinate")
        self.assertEqual(screen_coordinates.y, 200, "Wrong Y coordinate")

    @unittest.mock.patch('pygame.draw')
    def test_draw_vertexes_shouldCallTheDrawMethodOnTheDrawSurface(self, draw_surface):
        # Let's prepare the viewport to test
        width = 600
        height = 400
        viewport = Main.ViewPort.ViewPort(width, height, draw_surface)

        # The vertex list (only one)
        vertexes_list = (Vector2D(0, 0),)
        color = Main.Constants.WHITE
        viewport.draw_world_vertexes(vertexes_list, color)
        # Check the sequence passed to the draw_surface.line() call
        expected_sequence = ((300, 200),)
        self.assertSequenceEqual(draw_surface.lines.call_args[0][3], expected_sequence, "The sequences are not equal")

    def test_is_object_visible_anObjectVeryFarFromTheViewportCenter_shoudlBeNotVisible(self):
        # We have an object that is outside the viewport
        graph_object = GraphicObject(x=10000, y=10000, vertexes_local=(Vector2D(0, 0), Vector2D(10, 10)))

        width = 600
        height = 400
        viewport = Main.ViewPort.ViewPort(width, height, draw_surface=None)
        # TODO - Should test on the GrahpicObject, not on viewPort
        is_visible = viewport.is_object_visible(graph_object)
        self.assertFalse(is_visible, "the object should be not visible")

    def test_is_object_visible_anObjectInTheCenterOfTheViewportCenter_shoudlBeVisible(self):
        # We have an object that is in the center or the screen
        graph_object = GraphicObject(x=0, y=0, vertexes_local=(Vector2D(0, 0), Vector2D(10, 10)))

        width = 600
        height = 400
        viewport = Main.ViewPort.ViewPort(width, height, draw_surface=None)
        # TODO - Should test on the GrahpicObject, not on viewPort
        is_visible = viewport.is_object_visible(graph_object)
        self.assertTrue(is_visible, "the object should be visible")

if __name__ == "__main__":
    unittest.main()
