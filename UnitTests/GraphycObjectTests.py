'''
Created on 15/feb/2015

@author: Federico
'''
import unittest
import math
from Main import Values
from Main.GraphicObjects import GraphicObject


class GraphicObjectTests(unittest.TestCase):
    def test_move_shouldChangeThePositionOfTheObjectInTheCorrectWay(self):
        obj = GraphicObject()
        movement_angle = 45
        movement_length = 10
        
        expected_x = 10 / math.sqrt(2)
        expected_y = expected_x
        
        obj.move(movement_angle, movement_length)
        
        self.assertTrue(Values.are_equals(obj.x, expected_x), "The X coordinate is wrong")
        self.assertTrue(Values.are_equals(obj.y, expected_y), "The y coordinate is wrong")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()