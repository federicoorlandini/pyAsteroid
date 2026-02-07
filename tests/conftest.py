"""
Centralized test configuration for pyAsteroid.

This module handles:
- Python path setup for proper module imports
- Pygame mocking to allow tests to run without a display
- Common test utilities and base classes

Usage:
    All test files should import from this module first:
    
    from tests.conftest import GameTestCase, create_mock_world
    
    Or simply ensure this module is loaded by the test runner.
"""

import sys
import os
import unittest
import unittest.mock

# =============================================================================
# PATH SETUP - Must happen before any game module imports
# =============================================================================

# Get project root (parent of tests/ directory)
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_src_dir = os.path.join(_project_root, 'src')
_main_dir = os.path.join(_src_dir, 'Main')

# Add paths for imports
for _path in [_project_root, _src_dir, _main_dir]:
    if _path not in sys.path:
        sys.path.insert(0, _path)


# =============================================================================
# PYGAME MOCKING - Prevents display initialization errors in tests
# =============================================================================

def _create_pygame_mock():
    """Create a comprehensive pygame mock."""
    pygame_mock = unittest.mock.MagicMock()
    
    # Mock common pygame attributes
    pygame_mock.init = unittest.mock.MagicMock(return_value=(6, 0))
    pygame_mock.quit = unittest.mock.MagicMock()
    
    # Mock display
    pygame_mock.display = unittest.mock.MagicMock()
    pygame_mock.display.set_mode = unittest.mock.MagicMock(
        return_value=unittest.mock.MagicMock()
    )
    pygame_mock.display.update = unittest.mock.MagicMock()
    
    # Mock draw module
    pygame_mock.draw = unittest.mock.MagicMock()
    pygame_mock.draw.lines = unittest.mock.MagicMock()
    
    # Mock Surface and surface module
    pygame_mock.Surface = unittest.mock.MagicMock()
    pygame_mock.surface = unittest.mock.MagicMock()
    pygame_mock.surface.Surface = unittest.mock.MagicMock()
    
    # Mock font
    pygame_mock.font = unittest.mock.MagicMock()
    pygame_mock.font.SysFont = unittest.mock.MagicMock(
        return_value=unittest.mock.MagicMock()
    )
    
    # Mock time
    pygame_mock.time = unittest.mock.MagicMock()
    pygame_mock.time.Clock = unittest.mock.MagicMock()
    
    # Mock key
    pygame_mock.key = unittest.mock.MagicMock()
    pygame_mock.key.get_pressed = unittest.mock.MagicMock(
        return_value=[False] * 512
    )
    pygame_mock.key.set_repeat = unittest.mock.MagicMock()
    
    # Mock event
    pygame_mock.event = unittest.mock.MagicMock()
    pygame_mock.event.get = unittest.mock.MagicMock(return_value=[])
    
    # Mock locals (key constants)
    pygame_mock.locals = unittest.mock.MagicMock()
    pygame_mock.K_UP = 273
    pygame_mock.K_DOWN = 274
    pygame_mock.K_LEFT = 276
    pygame_mock.K_RIGHT = 275
    pygame_mock.K_SPACE = 32
    pygame_mock.K_ESCAPE = 27
    
    return pygame_mock


# Install pygame mock before any imports might try to use it
if 'pygame' not in sys.modules:
    _pygame_mock = _create_pygame_mock()
    sys.modules['pygame'] = _pygame_mock
    sys.modules['pygame.locals'] = _pygame_mock.locals
    sys.modules['pygame.draw'] = _pygame_mock.draw
    sys.modules['pygame.display'] = _pygame_mock.display
    sys.modules['pygame.font'] = _pygame_mock.font
    sys.modules['pygame.time'] = _pygame_mock.time
    sys.modules['pygame.key'] = _pygame_mock.key
    sys.modules['pygame.event'] = _pygame_mock.event
    sys.modules['pygame.surface'] = _pygame_mock.surface


# =============================================================================
# TEST UTILITIES
# =============================================================================

class GameTestCase(unittest.TestCase):
    """
    Base test class for pyAsteroid tests.
    
    Provides common setup, teardown, and utility methods for testing
    game components.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level fixtures."""
        pass
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass


# =============================================================================
# MOCK CLASSES - Shared across all test files
# =============================================================================

class MockWorld:
    """
    A lightweight mock World for testing game objects.
    
    This avoids the need to create a full World with all its dependencies
    when testing individual components.
    """
    
    def __init__(self, width=100, height=100):
        self._world_width = width
        self._world_height = height
        self._objects_list = {}
        self._objects_counter = 0
        self.starship = None
        
    def add_object(self, obj):
        """Add an object to the mock world."""
        self._objects_counter += 1
        obj.id = self._objects_counter
        self._objects_list[obj.id] = obj
        
    def get_objects_list(self):
        """Return the objects dictionary."""
        return self._objects_list
    
    def remove_object(self, obj_id):
        """Remove an object by ID."""
        if obj_id in self._objects_list:
            del self._objects_list[obj_id]


class MockConfiguration:
    """
    A mock configuration for testing.
    
    Supports all IConfiguration methods with safe type conversion
    and default value fallbacks.
    """
    
    def __init__(self, config_dict=None):
        self._config = config_dict or {}
        
    def get(self, key, default=None):
        return self._config.get(key, default)
    
    def get_int(self, key, default=0):
        value = self._config.get(key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def get_float(self, key, default=0.0):
        value = self._config.get(key, default)
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def get_color(self, key, default=(255, 255, 255)):
        return self._config.get(key, default)
    
    def get_vertexes(self, key, default=None):
        return self._config.get(key, default)
    
    def has(self, key):
        return self._config.get(key) is not None


class MockGameObjectFactory:
    """
    Mock factory for creating game objects in tests.
    
    Returns simple GraphicObjects that satisfy the factory interface
    without requiring configuration or physics dependencies.
    """
    
    def create_starship_at_origin(self):
        from graphicobjects import GraphicObject
        from geometrytransformation2d import Vector2D
        return GraphicObject(
            x=0, y=0,
            vertexes_local=[Vector2D(10, 0), Vector2D(-5, -5), Vector2D(-5, 5)]
        )
    
    def create_starship(self, x, y):
        from graphicobjects import GraphicObject
        from geometrytransformation2d import Vector2D
        return GraphicObject(
            x=x, y=y,
            vertexes_local=[Vector2D(10, 0), Vector2D(-5, -5), Vector2D(-5, 5)]
        )


class MockSystemFactory:
    """
    Mock factory for creating system components in tests.
    
    Returns MagicMock instances for asteroid generator and collision handler,
    allowing tests to verify interactions without real implementations.
    """
    
    def __init__(self):
        self._asteroid_generator = unittest.mock.MagicMock()
        self._asteroid_generator.process = unittest.mock.MagicMock()
        self._asteroid_generator.get_new_asteroid = unittest.mock.MagicMock(return_value=None)
        
        self._collision_handler = unittest.mock.MagicMock()
        self._collision_handler.handle = unittest.mock.MagicMock()
    
    def create_asteroid_generator(self, world):
        return self._asteroid_generator
    
    def create_collision_handler(self, world):
        return self._collision_handler


# =============================================================================
# FACTORY FUNCTIONS - Convenience functions for creating test objects
# =============================================================================

def create_mock_world(width=100, height=100):
    """
    Create a mock world for testing.
    
    Args:
        width: World width in pixels
        height: World height in pixels
        
    Returns:
        MockWorld instance
    """
    return MockWorld(width, height)


def create_test_vector(x=0, y=0):
    """
    Create a Vector2D for testing.
    
    Args:
        x: X coordinate
        y: Y coordinate
        
    Returns:
        Vector2D instance
    """
    from geometrytransformation2d import Vector2D
    return Vector2D(x, y)


def create_test_graphic_object(x=0, y=0, vertexes=None):
    """
    Create a GraphicObject for testing.
    
    Args:
        x: X position
        y: Y position
        vertexes: List of Vector2D vertexes (optional)
        
    Returns:
        GraphicObject instance
    """
    from graphicobjects import GraphicObject
    from geometrytransformation2d import Vector2D
    
    if vertexes is None:
        vertexes = [Vector2D(10, 10), Vector2D(-10, 10), 
                    Vector2D(-10, -10), Vector2D(10, -10)]
    
    return GraphicObject(x=x, y=y, vertexes_local=vertexes)
