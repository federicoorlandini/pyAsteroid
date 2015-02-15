'''
Created on 13/feb/2015

@author: Federico
'''

import math

def from_radiant_to_degree(angle_in_radiant):
    return angle_in_radiant * 180 / math.pi

def from_degree_to_radiant(angle_in_degree):
    return math.pi / 180 * angle_in_degree