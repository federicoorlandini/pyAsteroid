'''
Created on 15/feb/2015

@author: Federico
'''
import unittest
from Main import Values


class ValuesTests(unittest.TestCase):
    def test_AreSameValue_twoValuesThatDifferLessThanTheDelta_shouldReturnTrue(self):
        value1 = 1
        value2 = 1 + Values.VALUES_ARE_EQUALS_DELTA / 10
        areEquals = Values.are_equals(value1, value2)
        self.assertTrue(areEquals, "Values should be defined equal")
        
    def test_AreSameValue_twoValuesThatDifferMoreThanTheDelta_shouldReturnTrue(self):
        value1 = 1
        value2 = 1 + Values.VALUES_ARE_EQUALS_DELTA * 2
        areEquals = Values.are_equals(value1, value2)
        self.assertFalse(areEquals, "Values shouldn't be defined equal")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()