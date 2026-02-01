"""
Tests for the display module.
"""

import unittest
import unittest.mock

# Import test configuration (sets up paths and mocks)
import tests.conftest

from geometrytransformation2d import Vector2D
import constants
import display as display_module


class DisplayTests(unittest.TestCase):
    """Tests for Display class."""
    
    def test_to_display_coordinates_center_should_map_to_screen_center(self):
        """Viewport center (0,0) should map to screen center."""
        viewport_center = Vector2D(0, 0)
        width = 600
        height = 400
        
        mock_surface = unittest.mock.MagicMock()
        disp = display_module.Display(width=width, height=height, draw_surface=mock_surface)
        
        screen_coordinates = disp._to_display_coordinate(viewport_center)

        self.assertEqual(screen_coordinates.x, 300, "Wrong X coordinate")
        self.assertEqual(screen_coordinates.y, 200, "Wrong Y coordinate")
    
    def test_to_display_coordinates_positive_offset(self):
        """Positive world coordinates should map right and down from center."""
        point = Vector2D(50, 30)
        width = 600
        height = 400
        
        mock_surface = unittest.mock.MagicMock()
        disp = display_module.Display(width=width, height=height, draw_surface=mock_surface)
        
        screen_coordinates = disp._to_display_coordinate(point)
        
        # Center is (300, 200), so (50, 30) should map to (350, 230)
        self.assertEqual(screen_coordinates.x, 350)
        self.assertEqual(screen_coordinates.y, 230)
    
    def test_to_display_coordinates_negative_offset(self):
        """Negative world coordinates should map left and up from center."""
        point = Vector2D(-100, -50)
        width = 600
        height = 400
        
        mock_surface = unittest.mock.MagicMock()
        disp = display_module.Display(width=width, height=height, draw_surface=mock_surface)
        
        screen_coordinates = disp._to_display_coordinate(point)
        
        # Center is (300, 200), so (-100, -50) should map to (200, 150)
        self.assertEqual(screen_coordinates.x, 200)
        self.assertEqual(screen_coordinates.y, 150)

    def test_draw_world_vertexes_should_call_pygame_draw(self):
        """draw_world_vertexes should call pygame.draw.lines."""
        width = 600
        height = 400
        mock_surface = unittest.mock.MagicMock()
        
        disp = display_module.Display(width, height, mock_surface)

        vertexes_list = [Vector2D(0, 0), Vector2D(10, 0), Vector2D(10, 10)]
        color = constants.WHITE
        
        with unittest.mock.patch('pygame.draw.lines') as mock_lines:
            disp.draw_world_vertexes(vertexes_list, color)
            
            # pygame.draw.lines should have been called
            self.assertTrue(mock_lines.called)
    
    def test_draw_world_vertexes_converts_to_screen_coordinates(self):
        """draw_world_vertexes should convert world coords to screen coords."""
        width = 100
        height = 100
        mock_surface = unittest.mock.MagicMock()
        
        disp = display_module.Display(width, height, mock_surface)
        
        # Single vertex at origin
        vertexes_list = [Vector2D(0, 0)]
        color = constants.WHITE
        
        with unittest.mock.patch('pygame.draw.lines') as mock_lines:
            disp.draw_world_vertexes(vertexes_list, color)
            
            # Get the points argument (4th argument, index 3)
            call_args = mock_lines.call_args
            points = call_args[0][3]  # positional args, 4th element
            
            # Origin (0,0) should map to center (50, 50)
            self.assertEqual(points[0], (50, 50))
    
    def test_display_stores_dimensions(self):
        """Display should store width and height."""
        mock_surface = unittest.mock.MagicMock()
        disp = display_module.Display(width=800, height=600, draw_surface=mock_surface)
        
        self.assertEqual(disp.width, 800)
        self.assertEqual(disp.height, 600)
    
    def test_display_stores_draw_surface(self):
        """Display should store the draw surface."""
        mock_surface = unittest.mock.MagicMock()
        disp = display_module.Display(width=100, height=100, draw_surface=mock_surface)
        
        self.assertEqual(disp.draw_surface, mock_surface)


if __name__ == "__main__":
    unittest.main()
