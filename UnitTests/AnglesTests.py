'''
Created on 13/feb/2015

@author: Federico
'''
import unittest
import math
from Main import Angles
from Main import Values


class Test(unittest.TestCase):
    def test_from_radiant_to_degree_should_return_the_correct_value(self):
        angle_in_radiant = math.pi / 2
        angle_in_degree = Angles.from_radiant_to_degree(angle_in_radiant)
        
        self.assertTrue(Values.are_equals(angle_in_degree, 90), "Wrong angle")
        
    def test_from_degree_to_radiant_should_return_the_correct_value(self):
        angle_in_degree = 90
        expected_angle_in_radiant = math.pi / 2
        angle_in_radiant = Angles.from_degree_to_radiant(angle_in_degree)
        
        self.assertTrue(Values.are_equals(angle_in_radiant, expected_angle_in_radiant), "Wrong angle")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_ConvertToDegree']
    unittest.main()