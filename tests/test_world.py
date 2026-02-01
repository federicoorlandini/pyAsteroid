"""
Tests for the World class in engines module.
"""

import unittest
import unittest.mock

# Import test configuration (sets up paths and mocks)
import tests.conftest
from tests.conftest import MockConfiguration

from graphicobjects import GraphicObject
from geometrytransformation2d import Vector2D


class MockGameObjectFactory:
    """Mock factory for creating game objects in tests."""
    
    def create_starship_at_origin(self):
        return GraphicObject(
            x=0, y=0, 
            vertexes_local=[Vector2D(10, 0), Vector2D(-5, -5), Vector2D(-5, 5)]
        )


class MockSystemFactory:
    """Mock factory for creating system components in tests."""
    
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


# Import World after mocks are set up
from engines import World


class WorldTests(unittest.TestCase):
    """Tests for World class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game_object_factory = MockGameObjectFactory()
        self.system_factory = MockSystemFactory()
    
    def _create_world(self, width=100, height=100):
        """Helper to create a World with mocked dependencies."""
        return World(
            (width, height), 
            self.game_object_factory, 
            self.system_factory
        )

    def test_add_object_should_add_object_to_list(self):
        """add_object should add the object to the world's object list."""
        world = self._create_world()
        obj = GraphicObject()

        initial_count = len(world._objects_list)
        world.add_object(obj)

        self.assertEqual(len(world._objects_list), initial_count + 1)

    def test_is_object_visible_far_object_should_be_not_visible(self):
        """An object very far from viewport center should not be visible."""
        world = self._create_world(100, 100)
        graph_object = GraphicObject(
            x=10000, y=10000, 
            vertexes_local=(Vector2D(0, 0), Vector2D(10, 10))
        )
        
        is_visible = world._is_object_visible(graph_object)
        
        self.assertFalse(is_visible, "The object should not be visible")

    def test_is_object_visible_centered_object_should_be_visible(self):
        """An object at the center of the viewport should be visible."""
        width = 600
        height = 400
        world = self._create_world(width, height)
        graph_object = GraphicObject(
            x=0, y=0, 
            vertexes_local=(Vector2D(0, 0), Vector2D(10, 10))
        )
        
        is_visible = world._is_object_visible(graph_object)
        
        self.assertTrue(is_visible, "The object should be visible")

    def test_process_should_call_collision_handler(self):
        """process() should call collision handler's handle method."""
        world = self._create_world()
        
        world.process(1)
        
        self.assertTrue(self.system_factory._collision_handler.handle.called)
    
    def test_process_should_call_asteroid_generator(self):
        """process() should call asteroid generator's process method."""
        world = self._create_world()
        
        world.process(1)
        
        self.assertTrue(self.system_factory._asteroid_generator.process.called)
    
    def test_get_objects_list_returns_dictionary(self):
        """get_objects_list() should return the objects dictionary."""
        world = self._create_world()
        
        result = world.get_objects_list()
        
        self.assertIsInstance(result, dict)
    
    def test_add_object_assigns_unique_id(self):
        """Each added object should get a unique ID."""
        world = self._create_world()
        obj1 = GraphicObject()
        obj2 = GraphicObject()
        
        world.add_object(obj1)
        world.add_object(obj2)
        
        self.assertNotEqual(obj1.id, obj2.id)
    
    def test_world_initializes_with_starship(self):
        """World should have a starship after initialization."""
        world = self._create_world()
        
        self.assertIsNotNone(world.starship)
    
    def test_get_world_objects_list_returns_world_objects(self):
        """get_world_objects_list() should return renderable world objects."""
        world = self._create_world()
        
        result = world.get_world_objects_list()
        
        self.assertIsInstance(result, list)
        # Should have at least the starship
        self.assertGreaterEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
