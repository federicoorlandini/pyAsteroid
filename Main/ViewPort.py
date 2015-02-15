'''
Created on 07/dic/2014

@author: Federico
'''
from Main.Geometry2D import Vertex2D

class ViewPort(object):
    '''
    classdocs
    '''
    width = 0
    height = 0
    
    def __init__(self, width = 0, height = 0):
        self.width = width
        self.height = height
        
    def ToScreenCoordinate(self, x, y):
        viewportX = self.width / 2 + x
        viewportY = self.height / 2 +y
        return Vertex2D(viewportX, viewportY)
        