import math


class MovementHandler:
    def __init__(self, ball):
        self._ball = ball

    def decelerate(self):
        self._ball.velocity = max(self._ball.velocity - self._ball.acceleration, 0)

    def accelerate(self):
        self._ball.velocity += self._ball.acceleration

    def move(self):
        radians = math.radians(self._ball.direction)

        new_x = self._ball.center[0] + self._ball.velocity * math.cos(radians)
        new_y = self._ball.center[1] + self._ball.velocity * math.sin(radians)

        self._ball.center = (new_x, new_y)
        self.decelerate()
