'''
Created on 13/feb/2015

@author: Federico
'''
import unittest
from Main.LookupTable import CosSinTable
from Main.Geometry2D import Geometry2D
import math
from Main import LookupTable

class Test(unittest.TestCase):
    _lookupTable = LookupTable.CosSinTable()

    def test_from_radiant_to_degree_should_return_the_correct_value(self):
        angle_in_radiant = math.pi / 2
        table = CosSinTable()
        angle_in_degree = table.from_radiant_to_degree(angle_in_radiant)
        
        # We need this to access the vertex comparer
        geometry = Geometry2D(self._lookupTable)
        
        assert(geometry.areEquals(angle_in_degree, 90))
        
    def test_from_degree_to_radiant_should_return_the_correct_value(self):
        angle_in_degree = 90
        expected_angle_in_radiant = math.pi / 2
        table = CosSinTable()
        angle_in_radiant = table.from_degree_to_radiant(angle_in_degree)
        
        # We need this to access the vertex comparer
        geometry = Geometry2D(self._lookupTable)
        
        assert(geometry.areEquals(angle_in_radiant, expected_angle_in_radiant))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_ConvertToDegree']
    unittest.main()