import math

import constants


class BorderDetector:
    def __init__(self, ball):
        self._ball = ball

    def check_walls(self):
        radians = math.radians(self._ball.direction)

        far_point = [0, 0]

        if sign(math.cos(radians)) > 0:
            far_point[0] = max(self._ball.center[0] + self._ball.radius * math.cos(radians),
                               self._ball.center[0] + self._ball.radius * sign(math.cos(radians)))

        else:
            far_point[0] = min(self._ball.center[0] + self._ball.radius * math.cos(radians),
                               self._ball.center[0] + self._ball.radius * sign(math.cos(radians)))

        if sign(math.sin(radians)) > 0:
            far_point[1] = max(self._ball.center[1] + self._ball.radius * math.sin(radians),
                               self._ball.center[1] + self._ball.radius * sign(math.sin(radians)))
        else:
            far_point[1] = min(self._ball.center[1] + self._ball.radius * math.sin(radians),
                               self._ball.center[1] + self._ball.radius * sign(math.sin(radians)))

        if (far_point[0] <= constants.PADDING + constants.WALL_WIDTH or
                far_point[0] >= constants.SCREEN_WIDTH - constants.PADDING - constants.WALL_WIDTH):
            return "vertical"

        elif (far_point[1] <= constants.PADDING + constants.WALL_WIDTH or
              far_point[1] >= constants.SCREEN_HEIGHT - constants.PADDING - constants.WALL_WIDTH):
            return "horizontal"

        return None


def sign(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0
