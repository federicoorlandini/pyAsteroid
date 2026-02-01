"""
Tests for the AsteroidGenerator class in logic module.
"""

import unittest

# Import test configuration (sets up paths and mocks)
import tests.conftest
from tests.conftest import MockWorld

from logic import AsteroidGenerator
from graphicobjects import Asteroid


class AsteroidGeneratorTests(unittest.TestCase):
    """Tests for AsteroidGenerator class."""
    
    def test_process_should_decrease_countdown_counter(self):
        """process() should decrease the countdown counter."""
        initial_counter = 10
        world = MockWorld()
        generator = AsteroidGenerator(world, initial_counter, max_number_of_asteroid=10)
        
        generator.process()
        
        self.assertEqual(generator._countdown_counter, initial_counter - 1)

    def test_process_should_not_decrease_counter_below_zero(self):
        """process() should not decrease counter below zero."""
        initial_counter = 1
        world = MockWorld()
        generator = AsteroidGenerator(world, initial_counter, max_number_of_asteroid=10)
        
        generator.process()  # Counter becomes 0
        generator.process()  # Counter should stay at 0
        
        self.assertEqual(generator._countdown_counter, 0)

    def test_get_new_asteroid_returns_asteroid_when_countdown_expired(self):
        """get_new_asteroid() should return an asteroid when countdown is 0."""
        initial_counter = 0
        world = MockWorld()
        generator = AsteroidGenerator(world, initial_counter, max_number_of_asteroid=10)
        
        new_asteroid = generator.get_new_asteroid()
        
        self.assertIsNotNone(new_asteroid)
        self.assertIsInstance(new_asteroid, Asteroid)

    def test_get_new_asteroid_returns_none_when_countdown_not_expired(self):
        """get_new_asteroid() should return None when countdown > 0."""
        initial_counter = 5
        world = MockWorld()
        generator = AsteroidGenerator(world, initial_counter, max_number_of_asteroid=10)
        
        new_asteroid = generator.get_new_asteroid()
        
        self.assertIsNone(new_asteroid)
    
    def test_get_new_asteroid_respects_max_asteroid_limit(self):
        """get_new_asteroid() should not exceed max asteroid count."""
        world = MockWorld()
        generator = AsteroidGenerator(world, initial_countdown=0, max_number_of_asteroid=2)
        
        # Get first asteroid
        asteroid1 = generator.get_new_asteroid()
        self.assertIsNotNone(asteroid1)
        
        # Get second asteroid
        asteroid2 = generator.get_new_asteroid()
        self.assertIsNotNone(asteroid2)
        
        # Third should be None (max reached)
        asteroid3 = generator.get_new_asteroid()
        self.assertIsNone(asteroid3)
    
    def test_generate_starting_position_returns_tuple(self):
        """_generate_new_starting_position() should return x, y tuple."""
        world = MockWorld()
        generator = AsteroidGenerator(world, initial_countdown=0, max_number_of_asteroid=10)
        
        x, y = generator._generate_new_starting_position()
        
        self.assertIsInstance(x, (int, float))
        self.assertIsInstance(y, (int, float))
    
    def test_generate_speed_returns_positive_value(self):
        """_generate_speed() should return a positive speed."""
        world = MockWorld()
        generator = AsteroidGenerator(world, initial_countdown=0, max_number_of_asteroid=10)
        
        speed = generator._generate_speed()
        
        self.assertGreater(speed, 0)
    
    def test_generate_heading_returns_valid_angle(self):
        """_generate_heading() should return a valid angle."""
        world = MockWorld()
        generator = AsteroidGenerator(world, initial_countdown=0, max_number_of_asteroid=10)
        
        heading = generator._generate_heading()
        
        # Angle should be a number (could be any value for direction)
        self.assertIsInstance(heading, (int, float))
    
    def test_asteroid_counter_increments_on_new_asteroid(self):
        """_asteroid_counter should increment when new asteroid is created."""
        world = MockWorld()
        generator = AsteroidGenerator(world, initial_countdown=0, max_number_of_asteroid=10)
        
        initial_count = generator._asteroid_counter
        generator.get_new_asteroid()
        
        self.assertEqual(generator._asteroid_counter, initial_count + 1)


if __name__ == "__main__":
    unittest.main()
