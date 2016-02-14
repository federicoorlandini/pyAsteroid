import unittest
import math
from Main import Values
from Main.GraphicObjects import GraphicObject
from Main.GeometryTransformation2D import Vector2D
from Main.ViewPort import ViewPort


class GraphicObjectTests(unittest.TestCase):
    def test_move_shouldChangeThePositionOfTheObjectInTheCorrectWay(self):
        obj = GraphicObject()
        movement_angle = 45
        movement_length = 10
        
        expected_x = 10 / math.sqrt(2)
        expected_y = expected_x
        
        obj._move(movement_angle, movement_length)
        
        self.assertTrue(Values.are_equals(obj.position.x, expected_x), "The X coordinate is wrong")
        self.assertTrue(Values.are_equals(obj.position.y, expected_y), "The y coordinate is wrong")

    def test_rotate_shoudUpdateTheHeadAngleOfTheObject(self):
        obj = GraphicObject(vertexes_local= (Vector2D(1, 0),))
        rotation_angle = 45
        
        obj.rotate_head_direction(rotation_angle)

        # To be completed
        self.assertTrue(False, "to be implemented")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()