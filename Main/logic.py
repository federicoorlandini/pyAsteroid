from Main import constants
from Main.graphicobjects import Asteroid


class AsteroidGenerator:
    def __init__(self, world, initial_countdown, max_number_of_asteroid):
        self._initial_counter_value = initial_countdown
        self._countdown_counter = initial_countdown
        self._max_number_asteroid = max_number_of_asteroid
        self._asteroid_counter = 0
        self._world = world

    def process(self):
        self._countdown_counter -= 1
        self._countdown_counter = min(self._countdown_counter, 0)

    def get_new_asteroid(self):
        if self._countdown_counter <= 0 and self._asteroid_counter < self._max_number_asteroid:
            x, y = self._generate_new_starting_position()
            speed = self._generate_speed()
            angle = self._generate_heading()
            self._asteroid_counter += 1
            return Asteroid(self._world, x, y, angle, speed)
        else:
            return None

    def _generate_new_starting_position(self):
        x =  - constants.VIEWPORT_WIDTH / 2
        y = 0
        return x, y

    def _generate_speed(self):
        return 10

    def _generate_heading(self):
        return 0