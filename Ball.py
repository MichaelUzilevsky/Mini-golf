import math


class Ball:
    def __init__(self, center, radius, velocity, acceleration, direction):
        self._center = center
        self._radius = radius
        self._velocity = velocity
        self._acceleration = acceleration
        self._direction = direction

    # Getter for center
    @property
    def center(self):
        return self._center

    # Setter for center
    @center.setter
    def center(self, value):
        self._center = value

    # Getter for radius
    @property
    def radius(self):
        return self._radius

    # Setter for radius
    @radius.setter
    def radius(self, value):
        self._radius = value

    # Getter for velocity
    @property
    def velocity(self):
        return self._velocity

    # Setter for velocity
    @velocity.setter
    def velocity(self, value):
        self._velocity = value

    # Getter for acceleration
    @property
    def acceleration(self):
        return self._acceleration

    # Setter for acceleration
    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = value

    # Getter for direction
    @property
    def direction(self):
        return self._direction

    # Setter for direction
    @direction.setter
    def direction(self, value):
        self._direction = value

    def flip_direction(self, wall_type):
        if wall_type == 'horizontal':
            self.direction = -self.direction
        elif wall_type == 'vertical':
            self.direction = 180 - self.direction

        self.direction %= 360
