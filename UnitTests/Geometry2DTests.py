'''
Created on 09/feb/2015

@author: Federico
'''
import unittest
from Main.Geometry2D import Geometry2D, Vector2D
from Main import LookupTable
from math import sqrt
from Main import Values

class Point2DTests(unittest.TestCase):
    def test_add_shouldReturnTheCorrectValue(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(1, -1)
        v3 = v1.add(v2)
        self.assertEqual(v3.x, 2, "Wrong X coordinate for the vertex")
        self.assertEqual(v3.y, 1, "Wrong Y coordinate for the vertex")

class Geometry2DTests(unittest.TestCase):
    _lookupTable = LookupTable.CosSinTable()
        
    def test_rotate_positive_shouldReturnTheCorrectValue(self):
        test_vertex = Vector2D(1, 0)
        angle = 90
        
        geometry2D = Geometry2D(self._lookupTable)
        geometry2D.rotate(test_vertex, angle)
        
        self.assertTrue(Values.are_equals(test_vertex.x, 0), "The X coordinate should be equal")
        self.assertTrue(Values.are_equals(test_vertex.y, 1), "The y coordinate should be equal")

    def test_rotate_negative_shouldReturnTheCorrectValue(self):
        test_vertex = Vector2D(1, 0)
        angle = -90
        
        geometry_2d = Geometry2D(self._lookupTable)
        geometry_2d.rotate(test_vertex, angle)
        
        self.assertTrue(Values.are_equals(test_vertex.x, 0), "The X coordinate should be equal")
        self.assertTrue(Values.are_equals(test_vertex.y, -1), "The Y coordinate should be equal")
        
    def test_move_shouldReturnTheCorrectValue(self):
        test_vertex = Vector2D(1, 1)
        test_angle = 45
        test_length = 10
        
        expected_x = 1 + 10.0 / sqrt(2)
        expected_y = 1 - 10.0 / sqrt(2)     # Remember that the Y axe goes from the top to the bottom
        
        geometry_2d = Geometry2D(self._lookupTable)
        moved_vertex = geometry_2d.move(test_vertex, test_angle, test_length)
        
        self.assertTrue(Values.are_equals(moved_vertex.x, expected_x), "X are not equal")
        self.assertTrue(Values.are_equals(moved_vertex.y, expected_y), "Y are not equal")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()