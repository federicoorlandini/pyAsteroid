'''
Created on 09/feb/2015

@author: Federico
'''

class Point2D(object):
    x = 0
    y = 0
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def add(self, v):
        return Point2D(self.x + v.x, self.y + v.y)
    
class Geometry2D(object):
    '''
    classdocs
    '''
    
    def __init__(self, lookupTable):
        '''
        Constructor
        '''
        self._lookupTable = lookupTable
        
    def rotate(self, vertex, angle):
        if(angle < 0):
            sinSign = -1
        else:
            sinSign = 1
        
        angle = abs(angle)
        
        newX = vertex.x * self._lookupTable.cos[angle] - sinSign * vertex.y * self._lookupTable.sin[angle]
        newY = sinSign * vertex.x * self._lookupTable.sin[angle] + vertex.y * self._lookupTable.cos[angle]
        
        vertex.x = newX
        vertex.y = newY
        
    def move(self, vertex, angle_in_degree, length):
        new_x = vertex.x + self._lookupTable.cos[angle_in_degree] * length
        new_y = vertex.y - self._lookupTable.sin[angle_in_degree] * length
        return Point2D(new_x, new_y)