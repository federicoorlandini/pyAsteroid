"""
Tests for the factory classes.
"""

import unittest
import unittest.mock

# Import test configuration (sets up paths and mocks)
import tests.conftest
from tests.conftest import MockConfiguration, MockWorld

from Infrastructure.factories.system_factory import SystemFactory
from Infrastructure.factories.game_object_factory import GameObjectFactory
from Infrastructure.factories.physics_factory import PhysicsFactory
from Main.collisions import CollisionHandler
from Main.logic import AsteroidGenerator
from Main.graphicobjects import StarShip, Bullet, Asteroid
from Main.geometrytransformation2d import Vector2D, Circle


# --- SystemFactory Tests ---

class SystemFactoryTests(unittest.TestCase):
    """Tests for SystemFactory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = MockConfiguration({
            'game.asteroid.spawn_countdown': 50,
            'game.asteroid.max_count': 5,
            'display.width': 800,
            'display.height': 600,
            'display.fps': 60,
            'input.key_repeat_delay': 15,
            'input.key_repeat_interval': 20,
        })
        self.factory = SystemFactory(self.config)
    
    def test_create_collision_handler_returns_collision_handler(self):
        """create_collision_handler() should return a CollisionHandler."""
        mock_world = MockWorld()
        
        handler = self.factory.create_collision_handler(mock_world)
        
        self.assertIsInstance(handler, CollisionHandler)
    
    def test_create_asteroid_generator_returns_asteroid_generator(self):
        """create_asteroid_generator() should return an AsteroidGenerator."""
        mock_world = MockWorld()
        
        generator = self.factory.create_asteroid_generator(mock_world)
        
        self.assertIsInstance(generator, AsteroidGenerator)
    
    def test_create_asteroid_generator_uses_config_values(self):
        """create_asteroid_generator() should use configuration values."""
        mock_world = MockWorld()
        
        generator = self.factory.create_asteroid_generator(mock_world)
        
        # Check that config values were used
        self.assertEqual(generator._countdown_counter, 50)
        self.assertEqual(generator._max_number_asteroid, 5)
    
    def test_get_fps_returns_configured_value(self):
        """get_fps() should return the configured FPS value."""
        fps = self.factory.get_fps()
        
        self.assertEqual(fps, 60)
    
    def test_get_fps_returns_default_when_not_configured(self):
        """get_fps() should return default when not configured."""
        empty_config = MockConfiguration({})
        factory = SystemFactory(empty_config)
        
        fps = factory.get_fps()
        
        self.assertEqual(fps, 30)  # Default value
    
    def test_get_key_repeat_settings_returns_tuple(self):
        """get_key_repeat_settings() should return delay and interval tuple."""
        delay, interval = self.factory.get_key_repeat_settings()
        
        self.assertEqual(delay, 15)
        self.assertEqual(interval, 20)
    
    def test_get_world_bounds_returns_dimensions(self):
        """get_world_bounds() should return width and height tuple."""
        width, height = self.factory.get_world_bounds()
        
        self.assertEqual(width, 800)
        self.assertEqual(height, 600)


# --- GameObjectFactory Tests ---

class GameObjectFactoryTests(unittest.TestCase):
    """Tests for GameObjectFactory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = MockConfiguration({
            'game.starship.color': (255, 255, 255),
            'game.starship.reload_counter': 15,
            'game.bullet.speed': 200,
        })
        self.physics_factory = PhysicsFactory(self.config)
        self.factory = GameObjectFactory(self.config, self.physics_factory)
    
    def test_create_starship_returns_starship(self):
        """create_starship() should return a StarShip instance."""
        starship = self.factory.create_starship(10, 20)
        
        self.assertIsInstance(starship, StarShip)
    
    def test_create_starship_at_correct_position(self):
        """create_starship() should position starship correctly."""
        starship = self.factory.create_starship(100, 200)
        
        self.assertEqual(starship.position.x, 100)
        self.assertEqual(starship.position.y, 200)
    
    def test_create_starship_at_origin(self):
        """create_starship_at_origin() should create starship at (0, 0)."""
        starship = self.factory.create_starship_at_origin()
        
        self.assertEqual(starship.position.x, 0)
        self.assertEqual(starship.position.y, 0)
    
    def test_create_bullet_returns_bullet(self):
        """create_bullet() should return a Bullet instance."""
        bullet = self.factory.create_bullet(10, 20, 45)
        
        self.assertIsInstance(bullet, Bullet)
    
    def test_create_bullet_at_correct_position_and_angle(self):
        """create_bullet() should set position and angle correctly."""
        bullet = self.factory.create_bullet(50, 60, 90)
        
        self.assertEqual(bullet.position.x, 50)
        self.assertEqual(bullet.position.y, 60)
        self.assertEqual(bullet.head_angle, 90)
    
    def test_create_asteroid_returns_asteroid(self):
        """create_asteroid() should return an Asteroid instance."""
        asteroid = self.factory.create_asteroid(10, 20, 45, 30)
        
        self.assertIsInstance(asteroid, Asteroid)
    
    def test_create_asteroid_with_correct_properties(self):
        """create_asteroid() should set all properties correctly."""
        asteroid = self.factory.create_asteroid(100, 150, 180, 25)
        
        self.assertEqual(asteroid.position.x, 100)
        self.assertEqual(asteroid.position.y, 150)
        self.assertEqual(asteroid.head_angle, 180)
        self.assertEqual(asteroid.speed, 25)


# --- PhysicsFactory Tests ---

class PhysicsFactoryTests(unittest.TestCase):
    """Tests for PhysicsFactory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = MockConfiguration({
            'physics.collision_threshold': 0.001,
            'test.vector': [10.5, 20.5],
        })
        self.factory = PhysicsFactory(self.config)
    
    def test_create_vector_returns_vector2d(self):
        """create_vector() should return a Vector2D instance."""
        vector = self.factory.create_vector(5, 10)
        
        self.assertIsInstance(vector, Vector2D)
    
    def test_create_vector_with_correct_coordinates(self):
        """create_vector() should set coordinates correctly."""
        vector = self.factory.create_vector(15.5, 25.5)
        
        self.assertEqual(vector.x, 15.5)
        self.assertEqual(vector.y, 25.5)
    
    def test_create_circle_returns_circle(self):
        """create_circle() should return a Circle instance."""
        center = Vector2D(0, 0)
        
        circle = self.factory.create_circle(center, 10)
        
        self.assertIsInstance(circle, Circle)
    
    def test_create_circle_with_correct_properties(self):
        """create_circle() should set center and radius correctly."""
        center = Vector2D(5, 10)
        
        circle = self.factory.create_circle(center, 15)
        
        self.assertEqual(circle.center.x, 5)
        self.assertEqual(circle.center.y, 10)
        self.assertEqual(circle.radius, 15)
    
    def test_create_vector_from_config(self):
        """create_vector_from_config() should read from configuration."""
        vector = self.factory.create_vector_from_config('test.vector')
        
        self.assertEqual(vector.x, 10.5)
        self.assertEqual(vector.y, 20.5)
    
    def test_create_vector_from_config_uses_default(self):
        """create_vector_from_config() should use default when key missing."""
        vector = self.factory.create_vector_from_config('nonexistent', (1.0, 2.0))
        
        self.assertEqual(vector.x, 1.0)
        self.assertEqual(vector.y, 2.0)
    
    def test_get_collision_threshold(self):
        """get_collision_threshold() should return configured value."""
        threshold = self.factory.get_collision_threshold()
        
        self.assertEqual(threshold, 0.001)
    
    def test_get_collision_threshold_default(self):
        """get_collision_threshold() should return default when not configured."""
        empty_config = MockConfiguration({})
        factory = PhysicsFactory(empty_config)
        
        threshold = factory.get_collision_threshold()
        
        self.assertEqual(threshold, 0.0001)


if __name__ == "__main__":
    unittest.main()
