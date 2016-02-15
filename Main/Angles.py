import math


def from_radiant_to_degree(angle_in_radiant):
    """ Convert an angle from radiant to degree
    :param angle_in_radiant:
    """
    return angle_in_radiant * 180 / math.pi


def from_degree_to_radiant(angle_in_degree):
    """ Convert an angle from degree to radiant
    :param angle_in_degree:
    """
    return math.pi / 180 * angle_in_degree
