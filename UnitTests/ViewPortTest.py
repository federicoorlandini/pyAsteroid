'''
Created on 07/dic/2014

@author: Federico
'''
import unittest

import Main.ViewPort

class Test(unittest.TestCase):


    def test_ToScreenCoordinate_shouldReturnTheCorrectCoordinate(self):
        x = 0
        y = 0
        width = 600;
        height = 400;
        viewPort = Main.ViewPort.ViewPort(width = width, height = height)
        screenCoordinates = viewPort.ToScreenCoordinate(x, y)
        
        self.assertEqual(screenCoordinates.x, 300, "Wrong X coordinate")
        self.assertEqual(screenCoordinates.y, 200, "Wrong Y coordinate")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()