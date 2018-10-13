import unittest.mock
from geometrytransformation2d import Vector2D
import constants
from graphicobjects import GraphicObject
from engines import World


class DisplayTests(unittest.TestCase):
    def test_ToDisplayCoordinates_shouldReturnTheCorrectCoordinate(self):
        # center of the viewport
        viewport_center = Vector2D(0,0)
        width = 600
        height = 400
        display = display.Display(width=width, height=height)
        screen_coordinates = display._to_display_coordinate(viewport_center)

        # Should be mapped in the central point of the screen
        self.assertEqual(screen_coordinates.x, 300, "Wrong X coordinate")
        self.assertEqual(screen_coordinates.y, 200, "Wrong Y coordinate")

    @unittest.mock.patch('pygame.draw')
    def test_draw_vertexes_shouldCallTheDrawMethodOnTheDrawSurface(self, draw_surface):
        # Let's prepare the viewport to test
        width = 600
        height = 400
        display = display.Display(width, height, draw_surface)

        # The vertex list (only one)
        vertexes_list = (Vector2D(0, 0),)
        color = constants.WHITE
        display.draw_world_vertexes(vertexes_list, color)
        # Check the sequence passed to the draw_surface.line() call
        expected_sequence = ((300, 200),)
        self.assertSequenceEqual(draw_surface.lines.call_args[0][3], expected_sequence, "The sequences are not equal")

if __name__ == "__main__":
    unittest.main()
