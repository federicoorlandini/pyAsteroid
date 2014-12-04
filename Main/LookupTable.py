'''
Created on 13/mag/2014

@author: Federico
'''
import math

class CosSinTable(object):
    '''
    classdocs
    '''

    cos = object()
    sin = object()
    
    def __init__(self):
        '''
        Constructor
        '''
        cos = {}
        sin = {}
        for i in range(0, 359):
            ''' Convert in radiant '''
            angleRadiant = math.pi / 360 * i
            cos[i] = math.cos(angleRadiant)
            sin[i] = math.sin(angleRadiant)
        self.cos = cos
        self.sin = sin
        