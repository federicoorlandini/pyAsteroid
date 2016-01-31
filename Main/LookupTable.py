'''
Created on 13/mag/2014

@author: Federico
'''
import math
import Main.Angles


class CosSinTable(object):
    cos = None
    sin = None
    
    def __init__(self):
        cos = {}
        sin = {}
        for i in range(0, 359):
            ''' Convert in radiant '''
            angle_radiant = Main.Angles.from_degree_to_radiant(i)
            cos[i] = math.cos(angle_radiant)
            sin[i] = math.sin(angle_radiant)
        self.cos = cos
        self.sin = sin