"""
Tests for the graphicobjects module.
"""

import unittest
import unittest.mock
import math

# Import test configuration (sets up paths and mocks)
import tests.conftest
from tests.conftest import MockWorld, create_test_vector

import values
import constants
from graphicobjects import GraphicObject, StarShip, Bullet, Asteroid
from geometrytransformation2d import Vector2D


class GraphicObjectTests(unittest.TestCase):
    """Tests for GraphicObject class."""
    
    def test_move_should_change_position_correctly(self):
        """Moving an object at 45 degrees should update position correctly."""
        obj = GraphicObject()
        movement_angle = 45
        movement_length = 10

        expected_x = 10 / math.sqrt(2)
        expected_y = expected_x

        obj._move(movement_angle, movement_length)

        self.assertTrue(
            values.are_equals(obj.position.x, expected_x), 
            "The X coordinate is wrong"
        )
        self.assertTrue(
            values.are_equals(obj.position.y, expected_y), 
            "The Y coordinate is wrong"
        )

    def test_rotate_head_should_update_head_angle(self):
        """Rotating head direction should update head_angle."""
        obj = GraphicObject(vertexes_local=(Vector2D(1, 0),))
        rotation_angle = 45

        obj.rotate_head_direction(rotation_angle)

        self.assertEqual(obj.head_angle, rotation_angle)
    
    def test_rotate_head_should_wrap_around_360(self):
        """Head angle should wrap around at 360 degrees."""
        obj = GraphicObject()
        obj.head_angle = 350
        
        obj.rotate_head_direction(20)
        
        self.assertEqual(obj.head_angle, 10)

    def test_get_collision_circle_should_compute_correct_radius(self):
        """Collision circle radius should be max distance from origin."""
        # Prepare object with square vertexes centered at origin
        object_vertexes = (
            Vector2D(5, 5), Vector2D(5, -5), 
            Vector2D(-5, -5), Vector2D(-5, 5)
        )
        graph_object = GraphicObject(x=0, y=0, vertexes_local=object_vertexes)
        graph_object._compute_collision_circle()
        
        # Expected radius is diagonal distance from center to corner
        expected_radius = 5 * math.sqrt(2)
        
        self.assertTrue(
            values.are_equals(graph_object.collision_circle.radius, expected_radius)
        )

    @unittest.mock.patch.object(GraphicObject, '_compute_collision_circle')
    def test_process_should_update_collision_circle(self, mock_compute):
        """process() should call _compute_collision_circle."""
        object_vertexes = (
            Vector2D(5, 5), Vector2D(5, -5), 
            Vector2D(-5, -5), Vector2D(-5, 5)
        )
        graph_object = GraphicObject(x=0, y=0, vertexes_local=object_vertexes)
        
        # Reset mock after constructor call
        mock_compute.reset_mock()
        
        graph_object.process(1)
        
        self.assertTrue(mock_compute.called)
    
    def test_process_should_move_object_based_on_speed(self):
        """process() should move object by speed * delta_time."""
        obj = GraphicObject(x=0, y=0, vertexes_local=(Vector2D(1, 0),))
        obj.speed = 100  # 100 pixels per second
        obj.head_angle = 0  # Moving right
        
        obj.process(0.5)  # Half second
        
        # Should have moved 50 pixels in x direction
        self.assertTrue(values.are_equals(obj.position.x, 50))
    
    def test_get_vertexes_returns_object_vertexes(self):
        """get_vertexes() should return the object's vertex list."""
        vertexes = (Vector2D(1, 0), Vector2D(0, 1))
        obj = GraphicObject(vertexes_local=vertexes)
        
        result = obj.get_vertexes()
        
        self.assertEqual(len(result), 2)
    
    def test_get_color_returns_object_color(self):
        """get_color() should return the object's color."""
        obj = GraphicObject(color=constants.RED)
        
        self.assertEqual(obj.get_color(), constants.RED)


class StarShipTests(unittest.TestCase):
    """Tests for StarShip class."""

    def test_fire_with_reload_counter_not_zero_should_not_fire(self):
        """StarShip should not fire while reloading."""
        ship = StarShip(0, 0, constants.WHITE)
        ship.reload_counter = 1
        
        bullet = ship.fire()
        
        self.assertIsNone(bullet)

    def test_fire_with_reload_counter_zero_should_fire_bullet(self):
        """StarShip should fire when reload counter is zero."""
        ship = StarShip(0, 0, constants.WHITE)
        ship.reload_counter = 0
        
        bullet = ship.fire()
        
        self.assertIsNotNone(bullet)
        self.assertIsInstance(bullet, Bullet)

    def test_fire_should_reset_reload_counter(self):
        """Firing should reset the reload counter."""
        ship = StarShip(0, 0, constants.WHITE)
        ship.reload_counter = 0
        
        ship.fire()
        
        self.assertNotEqual(ship.reload_counter, 0)
        self.assertEqual(ship.reload_counter, StarShip.RELOAD_COUNTER_DEFAULT_VALUE)
    
    def test_is_reloading_returns_true_when_counter_positive(self):
        """is_reloading() should return True when counter > 0."""
        ship = StarShip(0, 0, constants.WHITE)
        ship.reload_counter = 5
        
        self.assertTrue(ship.is_reloading())
    
    def test_is_reloading_returns_false_when_counter_zero(self):
        """is_reloading() should return False when counter is 0."""
        ship = StarShip(0, 0, constants.WHITE)
        ship.reload_counter = 0
        
        self.assertFalse(ship.is_reloading())
    
    def test_process_should_decrease_reload_counter(self):
        """process() should decrease reload counter when reloading."""
        ship = StarShip(0, 0, constants.WHITE)
        initial_counter = 5
        ship.reload_counter = initial_counter
        
        ship.process(0.1)
        
        self.assertEqual(ship.reload_counter, initial_counter - 1)
    
    def test_rotate_object_should_also_rotate_head(self):
        """StarShip rotation should update both rotation_angle and head_angle."""
        ship = StarShip(0, 0, constants.WHITE)
        ship.head_angle = 0
        ship.rotation_angle = 0
        
        ship.rotate_object(45)
        
        self.assertEqual(ship.rotation_angle, 45)
        self.assertEqual(ship.head_angle, 45)


class BulletTests(unittest.TestCase):
    """Tests for Bullet class."""
    
    def test_bullet_should_have_correct_initial_direction(self):
        """Bullet should be created with specified direction."""
        bullet = Bullet(0, 0, angle_of_direction=45)
        
        self.assertEqual(bullet.head_angle, 45)
    
    def test_bullet_should_have_default_speed(self):
        """Bullet should have default speed of 150."""
        bullet = Bullet(0, 0, angle_of_direction=0)
        
        self.assertEqual(bullet.speed, 150)
    
    def test_bullet_with_custom_speed(self):
        """Bullet can be created with custom speed."""
        bullet = Bullet(0, 0, angle_of_direction=0, speed=200)
        
        self.assertEqual(bullet.speed, 200)


class AsteroidTests(unittest.TestCase):
    """Tests for Asteroid class."""
    
    def test_asteroid_should_have_correct_initial_properties(self):
        """Asteroid should be created with specified properties."""
        asteroid = Asteroid(10, 20, angle_of_direction=90, speed=50)
        
        self.assertEqual(asteroid.position.x, 10)
        self.assertEqual(asteroid.position.y, 20)
        self.assertEqual(asteroid.head_angle, 90)
        self.assertEqual(asteroid.speed, 50)
    
    def test_asteroid_collision_should_change_color(self):
        """Asteroid collision handler should change color to red."""
        asteroid = Asteroid(0, 0, angle_of_direction=0, speed=10)
        mock_world = MockWorld()
        mock_world.add_object(asteroid)
        
        # Create a mock collision info
        class MockCollisionInfo:
            first_collider_object_id = 1
            second_collider_object_id = 1
        
        asteroid.collision_handler(MockCollisionInfo(), mock_world)
        
        self.assertEqual(asteroid.color, constants.RED)


if __name__ == "__main__":
    unittest.main()
