import math
import Main.Angles


class CosSinTable(object):
    """ This class contains a lookup table for Sin and Cos values.
        The index in the array is the angle in degree """
    cos = None
    sin = None

    def __init__(self):
        cos = {}
        sin = {}
        # We compute the lookup table for positive angles and negative angles
        # to have an easier rotation algorithm
        for i in range(-359, 359):
            #  Convert in radiant
            angle_radiant = Main.Angles.from_degree_to_radiant(i)
            cos[i] = math.cos(angle_radiant)
            sin[i] = math.sin(angle_radiant)
        self.cos = cos
        self.sin = sin
