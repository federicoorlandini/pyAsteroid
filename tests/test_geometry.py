"""
Tests for the geometrytransformation2d module.
"""

import unittest
from math import sqrt

# Import test configuration (sets up paths and mocks)
import tests.conftest

import geometrytransformation2d
from geometrytransformation2d import Vector2D, Circle
import values


class Vector2DTests(unittest.TestCase):
    """Tests for Vector2D class."""
    
    def test_add_should_return_the_correct_value(self):
        """Adding two vectors should return the correct sum."""
        v1 = Vector2D(1, 2)
        v2 = Vector2D(1, -1)
        v3 = v1 + v2
        
        self.assertEqual(v3.x, 2, "Wrong X coordinate for the vertex")
        self.assertEqual(v3.y, 1, "Wrong Y coordinate for the vertex")

    def test_subtract_should_return_the_correct_value(self):
        """Subtracting two vectors should return the correct difference."""
        v1 = Vector2D(5, 3)
        v2 = Vector2D(2, 1)
        v3 = v1 - v2
        
        self.assertEqual(v3.x, 3, "Wrong X coordinate")
        self.assertEqual(v3.y, 2, "Wrong Y coordinate")

    def test_magnitude_power_2_should_return_the_correct_value(self):
        """magnitude_power_2 should return the squared length."""
        vector = Vector2D(1, 1)
        magnitude = vector.magnitude_power_2()
        
        self.assertTrue(values.are_equals(magnitude, 2))
    
    def test_magnitude_power_2_of_zero_vector(self):
        """Zero vector should have zero magnitude."""
        vector = Vector2D(0, 0)
        
        self.assertEqual(vector.magnitude_power_2(), 0)
    
    def test_magnitude_power_2_of_unit_vector(self):
        """Unit vector along x-axis should have magnitude squared of 1."""
        vector = Vector2D(1, 0)
        
        self.assertEqual(vector.magnitude_power_2(), 1)


class CircleTests(unittest.TestCase):
    """Tests for Circle class and collision detection."""
    
    def test_two_circles_far_apart_should_not_intersect(self):
        """Circles with centers farther than sum of radii should not intersect."""
        center_1 = Vector2D(0, 0)
        circle_1 = Circle(center_1, 2)
        center_2 = Vector2D(0, 4)
        circle_2 = Circle(center_2, 1)
        
        is_intersecting = circle_1.is_intersecting_circle(circle_2)
        
        self.assertFalse(is_intersecting)

    def test_two_circles_tangent_should_intersect(self):
        """Tangent circles (touching at one point) should intersect."""
        center_1 = Vector2D(0, 0)
        circle_1 = Circle(center_1, 1)
        center_2 = Vector2D(0, 2)
        circle_2 = Circle(center_2, 1)
        
        is_intersecting = circle_1.is_intersecting_circle(circle_2)
        
        self.assertTrue(is_intersecting)

    def test_two_circles_overlapping_should_intersect(self):
        """Overlapping circles should intersect."""
        center_1 = Vector2D(0, 0)
        circle_1 = Circle(center_1, 1)
        center_2 = Vector2D(0, 1)
        circle_2 = Circle(center_2, 1)
        
        is_intersecting = circle_1.is_intersecting_circle(circle_2)
        
        self.assertTrue(is_intersecting)
    
    def test_concentric_circles_should_intersect(self):
        """Concentric circles (same center) should intersect."""
        center = Vector2D(5, 5)
        circle_1 = Circle(center, 2)
        circle_2 = Circle(center, 3)
        
        self.assertTrue(circle_1.is_intersecting_circle(circle_2))


class GeometryTransformationTests(unittest.TestCase):
    """Tests for geometry transformation functions."""
    
    def test_rotate_positive_should_return_correct_value(self):
        """Rotating (1,0) by 90 degrees should give (0,1)."""
        test_vertex = Vector2D(1, 0)
        angle = 90

        rotated_vertex = geometrytransformation2d.rotate(test_vertex, angle)

        self.assertTrue(
            values.are_equals(rotated_vertex.x, 0), 
            "The rotated X coordinate should be equal to 0"
        )
        self.assertTrue(
            values.are_equals(rotated_vertex.y, 1), 
            "The rotated Y coordinate should be equal to 1"
        )

    def test_rotate_negative_should_return_correct_value(self):
        """Rotating (1,0) by -90 degrees should give (0,-1)."""
        test_vertex = Vector2D(1, 0)
        angle = -90

        rotated_vertex = geometrytransformation2d.rotate(test_vertex, angle)

        self.assertTrue(
            values.are_equals(rotated_vertex.x, 0), 
            "The rotated X coordinate should be equal to 0"
        )
        self.assertTrue(
            values.are_equals(rotated_vertex.y, -1), 
            "The rotated Y coordinate should be equal to -1"
        )

    def test_move_should_return_correct_value(self):
        """Moving a vertex at 45 degrees should update both coordinates."""
        test_vertex = Vector2D(1, 1)
        test_angle = 45
        test_length = 10

        expected_x = 1 + 10.0 / sqrt(2)
        expected_y = 1 + 10.0 / sqrt(2)

        moved_vertex = geometrytransformation2d.move_in_a_direction(
            test_vertex, test_angle, test_length
        )

        self.assertTrue(
            values.are_equals(moved_vertex.x, expected_x), 
            "X coordinates are not equal"
        )
        self.assertTrue(
            values.are_equals(moved_vertex.y, expected_y), 
            "Y coordinates are not equal"
        )
    
    def test_translate_should_move_vertex(self):
        """Translate should move vertex by given offsets."""
        vertex = Vector2D(5, 10)
        translated = geometrytransformation2d.translate(vertex, 3, -2)
        
        self.assertEqual(translated.x, 8)
        self.assertEqual(translated.y, 8)
    
    def test_from_local_to_world_with_no_rotation(self):
        """With zero rotation, local coordinates should just be translated."""
        local_vertex = Vector2D(5, 0)
        translation = Vector2D(10, 10)
        rotation = 0
        
        world_vertex = geometrytransformation2d.from_local_to_world_coordinates(
            local_vertex, translation, rotation
        )
        
        self.assertTrue(values.are_equals(world_vertex.x, 15))
        self.assertTrue(values.are_equals(world_vertex.y, 10))


if __name__ == "__main__":
    unittest.main()
