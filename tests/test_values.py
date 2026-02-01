"""
Tests for the values module.
"""

import unittest

# Import test configuration (sets up paths and mocks)
import tests.conftest

import values


class ValuesTests(unittest.TestCase):
    """Tests for value comparison functions."""
    
    def test_are_equals_two_values_that_differ_less_than_delta_should_return_true(self):
        """Two values differing less than the delta should be considered equal."""
        value1 = 1
        value2 = 1 + values.VALUES_ARE_EQUALS_DELTA / 10
        are_equals = values.are_equals(value1, value2)
        
        self.assertTrue(are_equals, "Values should be defined equal")
        
    def test_are_equals_two_values_that_differ_more_than_delta_should_return_false(self):
        """Two values differing more than the delta should not be considered equal."""
        value1 = 1
        value2 = 1 + values.VALUES_ARE_EQUALS_DELTA * 2
        are_equals = values.are_equals(value1, value2)
        
        self.assertFalse(are_equals, "Values shouldn't be defined equal")
    
    def test_are_equals_identical_values_should_return_true(self):
        """Identical values should be considered equal."""
        value1 = 42.0
        value2 = 42.0
        
        self.assertTrue(values.are_equals(value1, value2))
    
    def test_are_equals_negative_values(self):
        """Negative values close together should be considered equal."""
        value1 = -5.0
        value2 = -5.0 + values.VALUES_ARE_EQUALS_DELTA / 10
        
        self.assertTrue(values.are_equals(value1, value2))
    
    def test_are_equals_values_at_exact_delta_boundary(self):
        """Values exactly at the delta boundary should be considered equal."""
        value1 = 1.0
        value2 = 1.0 + values.VALUES_ARE_EQUALS_DELTA
        
        self.assertTrue(values.are_equals(value1, value2))


if __name__ == "__main__":
    unittest.main()
