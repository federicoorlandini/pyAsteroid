
VALUES_ARE_EQUALS_DELTA = 0.0001  # The minimum difference to consider two values as different


def are_equals(value1, value2):
    return abs(value1 - value2) <= VALUES_ARE_EQUALS_DELTA
