'''
Created on 15/feb/2015

@author: Federico
'''
import unittest
import math
from Main import Values
from Main.GraphicObjects import GraphicObject
from Main.Geometry2D import Point2D


class GraphicObjectTests(unittest.TestCase):
    def test_move_shouldChangeThePositionOfTheObjectInTheCorrectWay(self):
        obj = GraphicObject()
        movement_angle = 45
        movement_length = 10
        
        expected_x = 10 / math.sqrt(2)
        expected_y = - expected_x    # The X axis goes down
        
        obj.move(movement_angle, movement_length)
        
        self.assertTrue(Values.are_equals(obj.position.x, expected_x), "The X coordinate is wrong")
        self.assertTrue(Values.are_equals(obj.position.y, expected_y), "The y coordinate is wrong")

    def test_rotate_shoudMoveTheVertexInTheCorrectPlace(self):
        vertexes = (Point2D(1, 0), )
        obj = GraphicObject(vertexes= vertexes)
        rotation_angle = 45
        
        obj.rotate(rotation_angle)
        
        expected_vertex_x = 10 / math.sqrt(2)
        expected_vertex_y = - expected_vertex_x    # The X axis goes down
        
        self.assertTrue(Values.are_equals(obj._vertexes[0].x, expected_vertex_x), "Invalid X after rotation")
        self.assertEqual(Values.are_equals(obj._vertexes[0].y, expected_vertex_y), "Invalid Y after rotation")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()