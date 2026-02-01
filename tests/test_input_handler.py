"""
Tests for the input_handler module.
"""

import unittest
import unittest.mock

# Import test configuration (sets up paths and mocks)
import tests.conftest
from tests.conftest import MockWorld

import pygame
import pygame.locals
from input_handler import KeyboardInputHandler
from graphicobjects import StarShip, Bullet
from geometrytransformation2d import Vector2D
import constants

# Define key constants that might not be in mock
if not hasattr(pygame.locals, 'K_a'):
    pygame.locals.K_a = 97
if not hasattr(pygame.locals, 'K_d'):
    pygame.locals.K_d = 100
if not hasattr(pygame.locals, 'K_q'):
    pygame.locals.K_q = 113
if not hasattr(pygame.locals, 'K_SPACE'):
    pygame.locals.K_SPACE = 32
if not hasattr(pygame.locals, 'K_ESCAPE'):
    pygame.locals.K_ESCAPE = 27


class KeyboardInputHandlerTests(unittest.TestCase):
    """Tests for KeyboardInputHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_world = MockWorld()
        # Create a starship and add to world
        self.starship = StarShip(0, 0, constants.WHITE)
        self.mock_world.starship = self.starship
        self.mock_world.add_object(self.starship)
        
        self.handler = KeyboardInputHandler(self.mock_world)
    
    def _mock_keys(self, pressed_keys=None):
        """Helper to mock pygame.key.get_pressed()."""
        # Create a list of False values for all keys
        keys = [False] * 512
        if pressed_keys:
            for key in pressed_keys:
                keys[key] = True
        return keys
    
    def test_init_stores_world_reference(self):
        """Handler should store reference to world."""
        self.assertEqual(self.handler._world, self.mock_world)
    
    def test_init_exit_not_requested(self):
        """Handler should initialize with exit_requested as False."""
        self.assertFalse(self.handler._exit_requested)
    
    def test_is_exit_requested_returns_false_initially(self):
        """is_exit_requested() should return False initially."""
        self.assertFalse(self.handler.is_exit_requested())
    
    @unittest.mock.patch('pygame.key.get_pressed')
    def test_handle_input_rotate_left_with_a_key(self, mock_get_pressed):
        """Pressing 'A' key should rotate starship left (negative angle)."""
        # Use the actual key code value
        keys = self._mock_keys([97])  # K_a = 97
        mock_get_pressed.return_value = keys
        initial_angle = self.starship.rotation_angle
        
        # Also patch the pygame.locals reference used by input_handler
        with unittest.mock.patch.object(pygame.locals, 'K_a', 97):
            self.handler.handle_input()
        
        # Should rotate by -10 degrees
        expected_angle = (initial_angle - 10) % 360
        self.assertEqual(self.starship.rotation_angle, expected_angle)
    
    @unittest.mock.patch('pygame.key.get_pressed')
    def test_handle_input_rotate_right_with_d_key(self, mock_get_pressed):
        """Pressing 'D' key should rotate starship right (positive angle)."""
        # Use the actual key code value
        keys = self._mock_keys([100])  # K_d = 100
        mock_get_pressed.return_value = keys
        initial_angle = self.starship.rotation_angle
        
        # Also patch the pygame.locals reference used by input_handler
        with unittest.mock.patch.object(pygame.locals, 'K_d', 100):
            self.handler.handle_input()
        
        # Should rotate by 10 degrees
        expected_angle = (initial_angle + 10) % 360
        self.assertEqual(self.starship.rotation_angle, expected_angle)
    
    @unittest.mock.patch('pygame.key.get_pressed')
    def test_handle_input_fire_with_space_key(self, mock_get_pressed):
        """Pressing SPACE should fire a bullet when not reloading."""
        mock_get_pressed.return_value = self._mock_keys([pygame.locals.K_SPACE])
        self.starship.reload_counter = 0  # Not reloading
        initial_object_count = len(self.mock_world.get_objects_list())
        
        self.handler.handle_input()
        
        # A bullet should have been added to the world
        self.assertEqual(
            len(self.mock_world.get_objects_list()), 
            initial_object_count + 1
        )
    
    @unittest.mock.patch('pygame.key.get_pressed')
    def test_handle_input_no_fire_when_reloading(self, mock_get_pressed):
        """Pressing SPACE should not fire when reloading."""
        mock_get_pressed.return_value = self._mock_keys([pygame.locals.K_SPACE])
        self.starship.reload_counter = 5  # Still reloading
        initial_object_count = len(self.mock_world.get_objects_list())
        
        self.handler.handle_input()
        
        # No bullet should have been added
        self.assertEqual(
            len(self.mock_world.get_objects_list()), 
            initial_object_count
        )
    
    @unittest.mock.patch('pygame.key.get_pressed')
    def test_handle_input_exit_with_q_key(self, mock_get_pressed):
        """Pressing 'Q' key should request exit."""
        mock_get_pressed.return_value = self._mock_keys([pygame.locals.K_q])
        
        self.handler.handle_input()
        
        self.assertTrue(self.handler.is_exit_requested())
    
    @unittest.mock.patch('pygame.key.get_pressed')
    def test_handle_input_exit_with_escape_key(self, mock_get_pressed):
        """Pressing ESCAPE key should request exit."""
        mock_get_pressed.return_value = self._mock_keys([pygame.locals.K_ESCAPE])
        
        self.handler.handle_input()
        
        self.assertTrue(self.handler.is_exit_requested())
    
    @unittest.mock.patch('pygame.key.get_pressed')
    def test_handle_input_no_action_when_no_keys_pressed(self, mock_get_pressed):
        """No action should occur when no keys are pressed."""
        mock_get_pressed.return_value = self._mock_keys([])
        initial_angle = self.starship.rotation_angle
        initial_object_count = len(self.mock_world.get_objects_list())
        
        self.handler.handle_input()
        
        self.assertEqual(self.starship.rotation_angle, initial_angle)
        self.assertEqual(len(self.mock_world.get_objects_list()), initial_object_count)
        self.assertFalse(self.handler.is_exit_requested())
    
    @unittest.mock.patch('pygame.key.get_pressed')
    def test_handle_input_multiple_keys_simultaneously(self, mock_get_pressed):
        """Multiple keys pressed should all be processed."""
        # Press both A and D (should result in no net rotation since they cancel)
        mock_get_pressed.return_value = self._mock_keys([
            pygame.locals.K_a, 
            pygame.locals.K_d
        ])
        
        self.handler.handle_input()
        
        # Both rotations should have been applied (-10 + 10 = 0)
        self.assertEqual(self.starship.rotation_angle, 0)


if __name__ == "__main__":
    unittest.main()
