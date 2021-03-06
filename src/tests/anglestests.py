import unittest
import math
from src.Main import angles
from src.Main import values


class test_Angles(unittest.TestCase):
    def test_from_radiant_to_degree_should_return_the_correct_value(self):
        angle_in_radiant = math.pi / 2
        angle_in_degree = angles.from_radiant_to_degree(angle_in_radiant)
        
        self.assertTrue(values.are_equals(angle_in_degree, 90), "Wrong angle")
        
    def test_from_degree_to_radiant_should_return_the_correct_value(self):
        angle_in_degree = 90
        expected_angle_in_radiant = math.pi / 2
        angle_in_radiant = angles.from_degree_to_radiant(angle_in_degree)
        
        self.assertTrue(values.are_equals(angle_in_radiant, expected_angle_in_radiant), "Wrong angle")