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
        expected_y = - expected_x    # The X axis goes down
        
        obj.move(movement_angle, movement_length)
        
        self.assertTrue(Values.are_equals(obj.position.x, expected_x), "The X coordinate is wrong")
        self.assertTrue(Values.are_equals(obj.position.y, expected_y), "The y coordinate is wrong")

    def test_rotate_shoudMoveTheVertexInTheCorrectPlace(self):
        vertexes = (Vector2D(1, 0),)
        obj = GraphicObject(vertexes_local= vertexes)
        rotation_angle = 45
        
        obj.rotate(rotation_angle)
        
        expected_vertex_x = 1 / math.sqrt(2)
        expected_vertex_y = - expected_vertex_x    # The X axis goes down
        
        self.assertTrue(Values.are_equals(obj._vertexes_local[0].x, expected_vertex_x), "Invalid X after rotation")
        self.assertTrue(Values.are_equals(obj._vertexes_local[0].y, expected_vertex_y), "Invalid Y after rotation")


    def test_is_object_visible_anObjectVeryFarFromTheViewportCenter_shoudlBeNotVisible(self):
        # We have an object that is outside the viewport
        graph_object = GraphicObject(x=10000, y=10000, vertexes_local=(Vector2D(0, 0), Vector2D(10, 10)))

        width = 600
        height = 400
        viewport = ViewPort(width, height, draw_surface=None)
        # TODO - Should test on the GrahpicObject, not on viewPort
        is_visible = viewport.is_object_visible(graph_object)
        self.assertFalse(is_visible, "the object should be not visible")
'''
    def test_is_object_visible_anObjectInTheCenterOfTheViewportCenter_shoudlBeVisible(self):
        # We have an object that is in the center or the screen
        graph_object = GraphicObject(x=0, y=0, vertexes_local=(Vector2D(0, 0), Vector2D(10, 10)))

        width = 600
        height = 400
        viewport = ViewPort(width, height, draw_surface=None)
        # TODO - Should test on the GrahpicObject, not on viewPort
        is_visible = viewport.is_object_visible(graph_object)
        self.assertTrue(is_visible, "the object should be visible")
'''

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()