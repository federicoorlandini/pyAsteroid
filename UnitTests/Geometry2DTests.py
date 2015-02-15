'''
Created on 09/feb/2015

@author: Federico
'''
import unittest
from Main.Geometry2D import Geometry2D, Vertex2D
from Main import LookupTable
from math import sqrt

class Vertex2DTests(unittest.TestCase):
    def test_add_shouldReturnTheCorrectValue(self):
        v1 = Vertex2D(1, 2)
        v2 = Vertex2D(1, -1)
        v3 = v1.add(v2)
        assert(v3.x == 2)
        assert(v3.y == 1)

class Geometry2DTests(unittest.TestCase):
    _lookupTable = LookupTable.CosSinTable()

    def test_AreSameValue_twoValuesThatDifferLessThanTheDelta_shouldReturnTrue(self):
        geometry = Geometry2D(self._lookupTable)
        value1 = 1
        value2 = 1 + geometry.DELTA / 10
        areEquals = geometry.areEquals(value1, value2)
        assert(areEquals == True)
        
    def test_AreSameValue_twoValuesThatDifferMoreThanTheDelta_shouldReturnTrue(self):
        geometry = Geometry2D(self._lookupTable)
        value1 = 1
        value2 = 1 + geometry.DELTA * 2
        areEquals = geometry.areEquals(value1, value2)
        assert(areEquals == False)
        
    def test_rotate_positive_shouldReturnTheCorrectValue(self):
        testVertex = Vertex2D(1, 0)
        angle = 90
        
        geometry2D = Geometry2D(self._lookupTable)
        geometry2D.rotate(testVertex, angle)
        
        assert(geometry2D.areEquals(testVertex.x, 0))
        assert(geometry2D.areEquals(testVertex.y, 1))

    def test_rotate_negative_shouldReturnTheCorrectValue(self):
        testVertex = Vertex2D(1, 0)
        angle = -90
        
        geometry2D = Geometry2D(self._lookupTable)
        geometry2D.rotate(testVertex, angle)
        
        assert(geometry2D.areEquals(testVertex.x, 0))
        assert(geometry2D.areEquals(testVertex.y, -1))
        
    def test_move_shouldReturnTheCorrectValue(self):
        test_vertex = Vertex2D(1, 1)
        test_angle = 45
        test_length = 10
        
        expected_x = 1 + 10.0 / sqrt(2)
        expected_y = 1 - 10.0 / sqrt(2)     # Remember that the Y axe goes from the top to the bottom
        
        geometry2D = Geometry2D(self._lookupTable)
        moved_vertex = geometry2D.move(test_vertex, test_angle, test_length)
        
        self.assertTrue(geometry2D.areEquals(moved_vertex.x, expected_x), "X are not equal")
        self.assertTrue(geometry2D.areEquals(moved_vertex.y, expected_y), "Y are not equal")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()