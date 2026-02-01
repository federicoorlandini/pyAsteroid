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
    
    def test_process_adds_new_asteroid_from_generator(self):
        """process() should add new asteroid when generator provides one."""
        world = self._create_world()
        
        # Create a mock asteroid to be returned by generator
        mock_asteroid = GraphicObject(
            x=50, y=50, 
            vertexes_local=[Vector2D(5, 5), Vector2D(-5, 5), Vector2D(-5, -5), Vector2D(5, -5)]
        )
        self.system_factory._asteroid_generator.get_new_asteroid.return_value = mock_asteroid
        
        initial_count = len(world._objects_list)
        world.process(1)
        
        # A new asteroid should have been added
        self.assertEqual(len(world._objects_list), initial_count + 1)
    
    def test_remove_objects_not_visible_removes_far_objects(self):
        """_remove_objects_not_visible() should remove objects outside bounds."""
        world = self._create_world(100, 100)
        
        # Add an object that is way outside the viewport
        far_object = GraphicObject(
            x=10000, y=10000, 
            vertexes_local=[Vector2D(1, 1), Vector2D(-1, 1), Vector2D(-1, -1), Vector2D(1, -1)]
        )
        world.add_object(far_object)
        far_object_id = far_object.id
        
        # Verify it's in the world
        self.assertIn(far_object_id, world._objects_list)
        
        # Call remove
        world._remove_objects_not_visible()
        
        # Object should be removed
        self.assertNotIn(far_object_id, world._objects_list)
    
    def test_remove_objects_not_visible_keeps_visible_objects(self):
        """_remove_objects_not_visible() should keep objects inside bounds."""
        world = self._create_world(100, 100)
        
        # Add an object at the center (visible)
        visible_object = GraphicObject(
            x=0, y=0, 
            vertexes_local=[Vector2D(5, 5), Vector2D(-5, 5), Vector2D(-5, -5), Vector2D(5, -5)]
        )
        world.add_object(visible_object)
        visible_object_id = visible_object.id
        
        # Call remove
        world._remove_objects_not_visible()
        
        # Object should still be in the world
        self.assertIn(visible_object_id, world._objects_list)
    
    def test_get_world_vertexes_for_object_transforms_correctly(self):
        """_get_world_vertexes_for_object() should transform local to world coords."""
        world = self._create_world()
        
        # Create object at position (10, 20) with vertex at (5, 0)
        obj = GraphicObject(
            x=10, y=20,
            vertexes_local=[Vector2D(5, 0)]
        )
        obj.rotation_angle = 0  # No rotation
        
        world_vertexes = world._get_world_vertexes_for_object(obj)
        
        # Vertex (5, 0) + position (10, 20) = world (15, 20)
        self.assertEqual(len(world_vertexes), 1)
        self.assertAlmostEqual(world_vertexes[0].x, 15, places=5)
        self.assertAlmostEqual(world_vertexes[0].y, 20, places=5)
    
    def test_world_object_contains_vertexes_and_color(self):
        """World.WorldObject should contain vertexes and color."""
        vertexes = [Vector2D(1, 2), Vector2D(3, 4)]
        color = (255, 128, 64)
        
        world_object = World.WorldObject(vertexes, color)
        
        self.assertEqual(world_object.vertexes, vertexes)
        self.assertEqual(world_object.color, color)


if __name__ == "__main__":
    unittest.main()
