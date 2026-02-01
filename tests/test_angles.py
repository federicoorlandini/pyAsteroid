"""
Tests for the angles module.
"""

import unittest
import math

# Import test configuration (sets up paths and mocks)
import tests.conftest

from angles import from_radiant_to_degree, from_degree_to_radiant
import values


class AnglesTests(unittest.TestCase):
    """Tests for angle conversion functions."""
    
    def test_from_radiant_to_degree_should_return_the_correct_value(self):
        """Converting pi/2 radians should return 90 degrees."""
        angle_in_radiant = math.pi / 2
        angle_in_degree = from_radiant_to_degree(angle_in_radiant)
        
        self.assertTrue(
            values.are_equals(angle_in_degree, 90), 
            "Wrong angle: expected 90, got {}".format(angle_in_degree)
        )
        
    def test_from_degree_to_radiant_should_return_the_correct_value(self):
        """Converting 90 degrees should return pi/2 radians."""
        angle_in_degree = 90
        expected_angle_in_radiant = math.pi / 2
        angle_in_radiant = from_degree_to_radiant(angle_in_degree)
        
        self.assertTrue(
            values.are_equals(angle_in_radiant, expected_angle_in_radiant), 
            "Wrong angle: expected {}, got {}".format(
                expected_angle_in_radiant, angle_in_radiant
            )
        )
    
    def test_from_radiant_to_degree_zero_should_return_zero(self):
        """Converting 0 radians should return 0 degrees."""
        angle_in_radiant = 0
        angle_in_degree = from_radiant_to_degree(angle_in_radiant)
        
        self.assertTrue(
            values.are_equals(angle_in_degree, 0),
            "Zero radians should convert to zero degrees"
        )
    
    def test_from_degree_to_radiant_full_circle(self):
        """Converting 360 degrees should return 2*pi radians."""
        angle_in_degree = 360
        expected = 2 * math.pi
        angle_in_radiant = from_degree_to_radiant(angle_in_degree)
        
        self.assertTrue(
            values.are_equals(angle_in_radiant, expected),
            "360 degrees should convert to 2*pi radians"
        )


if __name__ == "__main__":
    unittest.main()
