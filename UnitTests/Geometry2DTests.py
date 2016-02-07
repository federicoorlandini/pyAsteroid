import unittest
from Main.GeometryTransformation2D import GeometryTransformation2D, Vector2D
from Main import LookupTable
from math import sqrt
from Main import Values


class Vector2DTests(unittest.TestCase):
    def test_add_shouldReturnTheCorrectValue(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(1, -1)
        v3 = v1.add(v2)
        self.assertEqual(v3.x, 2, "Wrong X coordinate for the vertex")
        self.assertEqual(v3.y, 1, "Wrong Y coordinate for the vertex")


class GeometryTransformation2DTests(unittest.TestCase):
    _lookupTable = LookupTable.CosSinTable()
        
    def test_rotate_positive_shouldReturnTheCorrectValue(self):
        # Vertex (1, 0) with a rotation of 90 degree (positive)
        test_vertex = Vector2D(1, 0)
        angle = 90
        
        geometry_2d = GeometryTransformation2D(self._lookupTable)
        rotated_vertex = geometry_2d.rotate(test_vertex, angle)

        # Should return the vertex (1, 1)
        self.assertTrue(Values.are_equals(rotated_vertex.x, 0), "The rotated X coordinate should be equal to 0")
        self.assertTrue(Values.are_equals(rotated_vertex.y, 1), "The rotated Y coordinate should be equal to 1")

    def test_rotate_negative_shouldReturnTheCorrectValue(self):
        # Vertex (1, 0) with a rotation of 90 degree (negative)
        test_vertex = Vector2D(1, 0)
        angle = -90
        
        geometry_2d = GeometryTransformation2D(self._lookupTable)
        rotated_vertex = geometry_2d.rotate(test_vertex, angle)

        # Should return the vertex (1, -1)
        self.assertTrue(Values.are_equals(rotated_vertex.x, 0), "The rotated X coordinate should be equal to 0")
        self.assertTrue(Values.are_equals(rotated_vertex.y, -1), "The rotated Y coordinate should be equal to -1")
        
    def test_move_shouldReturnTheCorrectValue(self):
        test_vertex = Vector2D(1, 1)
        test_angle = 45
        test_length = 10
        
        expected_x = 1 + 10.0 / sqrt(2)
        expected_y = 1 + 10.0 / sqrt(2)
        
        geometry_2d = GeometryTransformation2D(self._lookupTable)
        moved_vertex = geometry_2d.move_in_a_direction(test_vertex, test_angle, test_length)
        
        self.assertTrue(Values.are_equals(moved_vertex.x, expected_x), "X are not equal")
        self.assertTrue(Values.are_equals(moved_vertex.y, expected_y), "Y are not equal")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()