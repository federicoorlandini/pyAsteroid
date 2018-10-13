import unittest
import values


class ValuesTests(unittest.TestCase):
    def test_AreSameValue_twoValuesThatDifferLessThanTheDelta_shouldReturnTrue(self):
        value1 = 1
        value2 = 1 + values.VALUES_ARE_EQUALS_DELTA / 10
        are_equals = values.are_equals(value1, value2)
        self.assertTrue(are_equals, "Values should be defined equal")
        
    def test_AreSameValue_twoValuesThatDifferMoreThanTheDelta_shouldReturnTrue(self):
        value1 = 1
        value2 = 1 + values.VALUES_ARE_EQUALS_DELTA * 2
        are_equals = values.are_equals(value1, value2)
        self.assertFalse(are_equals, "Values shouldn't be defined equal")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()