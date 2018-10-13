import unittest
import geometrytransformation2d
from geometrytransformation2d import Vector2D
from math import sqrt
import values


class Vector2DTests(unittest.TestCase):
    def test_add_shouldReturnTheCorrectValue(self):
        v1 = Vector2D(1, 2)
        v2 = Vector2D(1, -1)
        v3 = v1 + v2
        self.assertEqual(v3.x, 2, "Wrong X coordinate for the vertex")
        self.assertEqual(v3.y, 1, "Wrong Y coordinate for the vertex")

    def test_magnitude_power_2_should_return_the_correct_value(self):
        vector = Vector2D(1, 1)
        magnitude = vector.magnitude_power_2()
        self.assertTrue(values.are_equals(magnitude, 2))


class GeometryTransformation2DTests(unittest.TestCase):
    def test_rotate_positive_shouldReturnTheCorrectValue(self):
        # Vertex (1, 0) with a rotation of 90 degree (positive)
        test_vertex = Vector2D(1, 0)
        angle = 90

        rotated_vertex = geometrytransformation2d.rotate(test_vertex, angle)

        # Should return the vertex (1, 1)
        self.assertTrue(values.are_equals(rotated_vertex.x, 0), "The rotated X coordinate should be equal to 0")
        self.assertTrue(values.are_equals(rotated_vertex.y, 1), "The rotated Y coordinate should be equal to 1")

    def test_rotate_negative_shouldReturnTheCorrectValue(self):
        # Vertex (1, 0) with a rotation of 90 degree (negative)
        test_vertex = Vector2D(1, 0)
        angle = -90

        rotated_vertex = geometrytransformation2d.rotate(test_vertex, angle)

        # Should return the vertex (1, -1)
        self.assertTrue(values.are_equals(rotated_vertex.x, 0), "The rotated X coordinate should be equal to 0")
        self.assertTrue(values.are_equals(rotated_vertex.y, -1), "The rotated Y coordinate should be equal to -1")

    def test_move_shouldReturnTheCorrectValue(self):
        test_vertex = Vector2D(1, 1)
        test_angle = 45
        test_length = 10

        expected_x = 1 + 10.0 / sqrt(2)
        expected_y = 1 + 10.0 / sqrt(2)

        moved_vertex = geometrytransformation2d.move_in_a_direction(test_vertex, test_angle, test_length)

        self.assertTrue(values.are_equals(moved_vertex.x, expected_x), "X are not equal")
        self.assertTrue(values.are_equals(moved_vertex.y, expected_y), "Y are not equal")

    def test_two_circles_with_centers_more_far_than_the_sum_of_the_two_radius_should_not_intersect(self):
        center_1 = Vector2D(0, 0)
        circle_1 = geometrytransformation2d.Circle(center_1, 2)
        center_2 = Vector2D(0, 4)
        circle_2 = geometrytransformation2d.Circle(center_2, 1)
        is_intersecting = circle_1.is_intersecting_circle(circle_2)
        self.assertFalse(is_intersecting)

    def test_two_circles_tangent_should_intersect(self):
        center_1 = Vector2D(0, 0)
        circle_1 = geometrytransformation2d.Circle(center_1, 1)
        center_2 = Vector2D(0, 2)
        circle_2 = geometrytransformation2d.Circle(center_2, 1)
        is_intersecting = circle_1.is_intersecting_circle(circle_2)
        self.assertTrue(is_intersecting)

    def test_two_circles_with_centers_closer_than_the_sum_of_the_two_radius_should_intersect(self):
        center_1 = Vector2D(0, 0)
        circle_1 = geometrytransformation2d.Circle(center_1, 1)
        center_2 = Vector2D(0, 1)
        circle_2 = geometrytransformation2d.Circle(center_2, 1)
        is_intersecting = circle_1.is_intersecting_circle(circle_2)
        self.assertTrue(is_intersecting)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
