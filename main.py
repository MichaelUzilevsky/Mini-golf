import time
import constants
from Ball import Ball
from movement_handler import MovementHandler
from border_detector import BorderDetector
import pygame
import math


def calculate_velocity_and_direction(start_drag, end_drag):
    velocity = min(15, int(0.1 * math.sqrt((end_drag[0] - start_drag[0]) ** 2 + (end_drag[1] - start_drag[1]) ** 2)))
    direction = math.atan2((end_drag[1] - start_drag[1]), (end_drag[0] - start_drag[0]))
    direction_degrees = int(math.degrees(direction)) + 180
    return velocity, direction_degrees


def handle_mouse_down(event, ball):
    mouse_pos = pygame.mouse.get_pos()
    distance_from_center = math.sqrt((mouse_pos[0] - ball.center[0]) ** 2 + (mouse_pos[1] - ball.center[1]) ** 2)
    if distance_from_center <= ball.radius and ball.velocity == 0:
        return True, mouse_pos  # Start dragging
    return False, None


def handle_mouse_up(event, dragging, start_drag, ball):
    if dragging:
        end_drag = pygame.mouse.get_pos()
        velocity, direction = calculate_velocity_and_direction(start_drag, end_drag)
        ball.direction = direction
        ball.velocity = velocity
    return False  # Stop dragging


def handle_mouse_motion(screen, dragging, start_drag, ball):
    if dragging:
        screen.fill(constants.BACKGROUND_COLOR)
        draw_walls(screen)
        pygame.draw.circle(screen, constants.BALL_COLOR, ball.center, ball.radius)
        update_trajectory(screen, ball, start_drag)


def update_trajectory(screen, ball, start_drag):
    curr_pos = pygame.mouse.get_pos()
    velocity, direction = calculate_velocity_and_direction(start_drag, curr_pos)
    simulate_trajectory(screen, ball.center, direction, velocity, ball.acceleration)


def simulate_trajectory(screen, position, direction, velocity, acceleration):
    distance_left = calculate_distance_traveled(velocity, acceleration)
    while distance_left > 0:
        impact_wall = find_impact_wall(position, velocity, direction)
        distance = find_distance_to_wall(impact_wall, position, direction)
        distance_to_draw = min(distance, distance_left)
        position = draw_line(screen, position, direction, distance_to_draw)
        distance_left -= distance_to_draw
        if impact_wall in ['top', 'bottom']:
            direction = -direction
        else:
            direction = 180 - direction
        direction %= 360


def handle_events(screen, active, ball, dragging, start_drag):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, dragging, start_drag

        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging, start_drag = handle_mouse_down(event, ball)

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = handle_mouse_up(event, dragging, start_drag, ball)

        elif event.type == pygame.MOUSEMOTION:
            handle_mouse_motion(screen, dragging, start_drag, ball)

    return active, dragging, start_drag


# not efficient
def expected_route_super_accurate(screen, position, angle, velocity, acceleration):
    mini_ball = Ball(position, constants.BALL_RADIUS * 0.75, velocity, acceleration, angle)
    movement_handler = MovementHandler(mini_ball)
    border_detector = BorderDetector(mini_ball)
    while mini_ball.velocity > 0:
        pygame.draw.circle(screen, constants.PREDICTOR_COLOR, mini_ball.center, mini_ball.radius)
        pygame.display.update()
        movement_handler.move()
        wall = border_detector.check_walls()
        if wall:
            mini_ball.flip_direction(wall)


def calculate_distance_traveled(velocity, acceleration):
    return (velocity ** 2) / (2 * acceleration)


def find_impact_wall(position, velocity, angle):
    radian_angle = math.radians(angle)
    vy = velocity * math.sin(radian_angle)
    vx = velocity * math.cos(radian_angle)

    top_distance = position[1]
    bottom_distance = constants.SCREEN_HEIGHT - constants.WALL_WIDTH - constants.PADDING - position[1]
    left_distance = position[0]
    right_distance = constants.SCREEN_WIDTH - constants.WALL_WIDTH - constants.PADDING - position[0]

    time_to_top = float('inf') if vy >= 0 else (top_distance / -vy)
    time_to_bottom = float('inf') if vy <= 0 else (bottom_distance / vy)
    time_to_left = float('inf') if vx >= 0 else (left_distance / -vx)
    time_to_right = float('inf') if vx <= 0 else (right_distance / vx)

    min_time = min(time_to_top, time_to_bottom, time_to_left, time_to_right)

    if min_time == time_to_top:
        return 'top'
    elif min_time == time_to_bottom:
        return 'bottom'
    elif min_time == time_to_left:
        return 'left'
    elif min_time == time_to_right:
        return 'right'


def find_distance_to_wall(impact_wall, position, angle):
    radian_angle = math.radians(angle)
    sin_angle = math.sin(radian_angle)
    cos_angle = math.cos(radian_angle)
    distance = float('inf')

    if impact_wall == 'top' and sin_angle != 0:
        distance = (position[1] - constants.WALL_WIDTH - constants.PADDING) / sin_angle
    elif impact_wall == 'bottom' and sin_angle != 0:
        distance = ((constants.SCREEN_HEIGHT - constants.WALL_WIDTH - constants.PADDING - position[1]) / sin_angle)
    elif impact_wall == 'left' and cos_angle != 0:
        distance = (position[0] - constants.WALL_WIDTH - constants.PADDING) / cos_angle
    elif impact_wall == 'right' and cos_angle != 0:
        distance = ((constants.SCREEN_WIDTH - constants.WALL_WIDTH - constants.PADDING - position[0]) / cos_angle)

    return abs(distance)  # Use absolute value to avoid negative distances


def draw_line(screen, starting_position, angle, distance):
    radian_angle = math.radians(angle)
    end_x = starting_position[0] + distance * math.cos(radian_angle)
    end_y = starting_position[1] + distance * math.sin(radian_angle)

    pygame.draw.line(screen, (255, 0, 0), starting_position, (end_x, end_y), 2)
    return end_x, end_y


def update_game_state(screen, game_ball, movement_handler, border_detector, background_color):
    if game_ball.velocity != 0:
        screen.fill(background_color)
        draw_walls(screen)
    pygame.draw.circle(screen, constants.BALL_COLOR, game_ball.center, game_ball.radius)
    pygame.display.update()
    movement_handler.move()
    wall = border_detector.check_walls()
    if wall:
        game_ball.flip_direction(wall)


def maintain_frame_rate(start_time, interval):
    elapsed_time = time.time() - start_time
    time_to_wait = interval - elapsed_time
    if time_to_wait > 0:
        time.sleep(time_to_wait)


def draw_walls(screen):
    borders = pygame.Rect(constants.PADDING, constants.PADDING, (constants.SCREEN_WIDTH - 2 * constants.PADDING),
                          (constants.SCREEN_HEIGHT - 2 * constants.PADDING))
    pygame.draw.rect(screen, constants.BALL_COLOR, borders, constants.WALL_WIDTH, 20)


def main():
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    active = True
    background_color = constants.BACKGROUND_COLOR
    screen.fill(background_color)
    draw_walls(screen)

    game_ball = Ball(constants.STARTING_POSITION, constants.BALL_RADIUS, 0, 0.04, 0)
    movement_handler = MovementHandler(game_ball)
    border_detector = BorderDetector(game_ball)

    interval = 0.015  # Set the desired frame interval

    dragging = False
    start_drag = [0, 0]

    while active:
        start_time = time.time()

        active, dragging, start_drag = handle_events(screen, active, game_ball, dragging, start_drag)
        update_game_state(screen, game_ball, movement_handler, border_detector, background_color)
        maintain_frame_rate(start_time, interval)

    pygame.quit()


if __name__ == '__main__':
    main()
