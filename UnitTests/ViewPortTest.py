'''
Created on 07/dic/2014

@author: Federico
'''
import unittest.mock
import Main.ViewPort
from Main.Geometry2D import Vector2D
import Main.Constants


class ViewPortTests(unittest.TestCase):
    def test_ToScreenCoordinate_shouldReturnTheCorrectCoordinate(self):
        # center of the viewport
        x = 0
        y = 0
        width = 600;
        height = 400;
        viewPort = Main.ViewPort.ViewPort(width=width, height=height)
        screenCoordinates = viewPort.to_screen_coordinate(x, y)

        # Should be mapped in the central point of the screen
        self.assertEqual(screenCoordinates.x, 300, "Wrong X coordinate")
        self.assertEqual(screenCoordinates.y, 200, "Wrong Y coordinate")

    @unittest.mock.patch('pygame.draw')
    def test_draw_vertexes_shouldCallTheDrawMethodOnTheDrawSurface(self, draw_surface):
        # Let's prepare the viewport to test
        width = 600;
        height = 400;
        viewPort = Main.ViewPort.ViewPort(width, height, draw_surface)

        # The vertex list (only one)
        vertexes_list = (Vector2D(0, 0),)
        position_x = 0
        position_y = 0
        color = Main.Constants.WHITE
        viewPort.draw_vertexes(position_x, position_y, vertexes_list, color)
        # Check the sequence passed to the draw_surface.line() call
        expected_sequence = ((300, 200),)
        self.assertSequenceEqual(draw_surface.lines.call_args[0][3], expected_sequence, "The sequences are not equal")


if __name__ == "__main__":
    unittest.main()
