"""
Tests for the collision handling module.
"""

import unittest
import unittest.mock

# Import test configuration (sets up paths and mocks)
import tests.conftest
from tests.conftest import MockWorld

from graphicobjects import GraphicObject, Bullet, Asteroid
from geometrytransformation2d import Vector2D
from collisions import CollisionHandler, CollisionInfo


class CollisionInfoTests(unittest.TestCase):
    """Tests for CollisionInfo class."""
    
    def test_collision_info_stores_object_ids(self):
        """CollisionInfo should store both collider object IDs."""
        info = CollisionInfo(first_collider_object_id=1, second_collider_object_id=2)
        
        self.assertEqual(info.first_collider_object_id, 1)
        self.assertEqual(info.second_collider_object_id, 2)


class CollisionHandlerTests(unittest.TestCase):
    """Tests for CollisionHandler class."""
    
    def _create_square_object(self, x, y, size=10):
        """Helper to create a square GraphicObject."""
        half = size / 2
        vertexes = [
            Vector2D(half, half), Vector2D(half, -half),
            Vector2D(-half, -half), Vector2D(-half, half)
        ]
        return GraphicObject(x=x, y=y, vertexes_local=vertexes)
    
    def test_handle_with_no_objects_should_not_raise(self):
        """handle() should work with empty world."""
        world = MockWorld()
        handler = CollisionHandler(world)
        
        # Should not raise
        handler.handle()
    
    def test_handle_with_non_colliding_objects_should_not_call_collision_handler(self):
        """handle() should not call collision_handler when objects don't collide."""
        world = MockWorld()
        
        # Create two objects far apart
        obj1 = self._create_square_object(0, 0, size=10)
        obj2 = self._create_square_object(100, 100, size=10)
        
        # Mock collision handlers
        obj1.collision_handler = unittest.mock.MagicMock()
        obj2.collision_handler = unittest.mock.MagicMock()
        
        world.add_object(obj1)
        world.add_object(obj2)
        
        handler = CollisionHandler(world)
        handler.handle()
        
        # Neither should have been called
        obj1.collision_handler.assert_not_called()
        obj2.collision_handler.assert_not_called()
    
    def test_handle_with_colliding_objects_should_call_collision_handlers(self):
        """handle() should call collision_handler on colliding objects."""
        world = MockWorld()
        
        # Create two overlapping objects
        obj1 = self._create_square_object(0, 0, size=20)
        obj2 = self._create_square_object(5, 5, size=20)
        
        # Mock collision handlers
        obj1.collision_handler = unittest.mock.MagicMock()
        obj2.collision_handler = unittest.mock.MagicMock()
        
        world.add_object(obj1)
        world.add_object(obj2)
        
        handler = CollisionHandler(world)
        handler.handle()
        
        # Both should have been called
        self.assertTrue(obj1.collision_handler.called)
        self.assertTrue(obj2.collision_handler.called)
    
    def test_build_collision_list_returns_empty_for_no_collisions(self):
        """_build_collision_list should return empty dict when no collisions."""
        world = MockWorld()
        
        obj1 = self._create_square_object(0, 0, size=10)
        obj2 = self._create_square_object(100, 100, size=10)
        
        world.add_object(obj1)
        world.add_object(obj2)
        
        handler = CollisionHandler(world)
        collisions = handler._build_collision_list()
        
        self.assertEqual(len(collisions), 0)
    
    def test_build_collision_list_detects_overlapping_objects(self):
        """_build_collision_list should detect overlapping objects."""
        world = MockWorld()
        
        # Create overlapping objects
        obj1 = self._create_square_object(0, 0, size=20)
        obj2 = self._create_square_object(5, 5, size=20)
        
        world.add_object(obj1)
        world.add_object(obj2)
        
        handler = CollisionHandler(world)
        collisions = handler._build_collision_list()
        
        # Both objects should be in collision list
        self.assertEqual(len(collisions), 2)
    
    def test_single_object_should_not_collide_with_itself(self):
        """A single object should not register a collision with itself."""
        world = MockWorld()
        
        obj = self._create_square_object(0, 0, size=10)
        world.add_object(obj)
        
        handler = CollisionHandler(world)
        collisions = handler._build_collision_list()
        
        self.assertEqual(len(collisions), 0)
    
    def test_three_overlapping_objects_all_detected(self):
        """Three overlapping objects should all have collisions detected."""
        world = MockWorld()
        
        # Create three overlapping objects at origin
        obj1 = self._create_square_object(0, 0, size=20)
        obj2 = self._create_square_object(5, 0, size=20)
        obj3 = self._create_square_object(0, 5, size=20)
        
        obj1.collision_handler = unittest.mock.MagicMock()
        obj2.collision_handler = unittest.mock.MagicMock()
        obj3.collision_handler = unittest.mock.MagicMock()
        
        world.add_object(obj1)
        world.add_object(obj2)
        world.add_object(obj3)
        
        handler = CollisionHandler(world)
        handler.handle()
        
        # All three should have collision handlers called
        self.assertTrue(obj1.collision_handler.called)
        self.assertTrue(obj2.collision_handler.called)
        self.assertTrue(obj3.collision_handler.called)


if __name__ == "__main__":
    unittest.main()
