import unittest
import logic

class AsteroidGeneratorTest(unittest.TestCase):
    def process_should_decrease_the_generator_counter(self):
        initial_counter = 10
        generator = logic.AsteroidGenerator(initial_counter, 10)
        generator.process()
        self.assertEqual(generator._countdown_counter, initial_counter - 1)

    def process_should_decrease_the_generator_counter_but_not_below_zero(self):
        initial_counter = 1
        generator = logic.AsteroidGenerator(initial_counter, 10)
        generator.process() # Now countdown_counter should be zero
        generator.process() # countdown_counter should not go below zero
        self.assertEqual(generator._countdown_counter, 0)

    def get_new_asteroid_return_a_new_asteroid_if_the_countdown_expired(self):
        initial_counter = 0
        generator = logic.AsteroidGenerator(initial_counter, 10)
        new_asteroid = generator.get_new_asteroid()
        self.assertIsNotNone(new_asteroid)

    def get_new_asteroid_return_none_if_the_countdown_is_not_expired(self):
        initial_counter = 1
        generator = logic.AsteroidGenerator(initial_counter, 10)
        new_asteroid = generator.get_new_asteroid()
        self.assertIsNone(new_asteroid)