import pygame
import pymunk
import pymunk.pygame_util

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Setup screen and physics space
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rube Goldberg Machine")
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

def create_ball(space, pos, radius=20):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, radius))
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.8
    space.add(body, shape)
    return body

def create_static_segment(space, start, end):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, start, end, 5)
    shape.elasticity = 0.8
    space.add(body, shape)

def create_domino(space, pos):
    body = pymunk.Body(1, pymunk.moment_for_box(1, (10, 40)))
    body.position = pos
    shape = pymunk.Poly.create_box(body, (10, 40))
    shape.elasticity = 0.4
    space.add(body, shape)
    return body

def create_lever(space, pivot_pos, beam_pos):
    beam = pymunk.Body(5, pymunk.moment_for_box(5, (100, 10)))
    beam.position = beam_pos
    shape = pymunk.Poly.create_box(beam, (100, 10))
    shape.elasticity = 0.6
    pivot = pymunk.Body(body_type=pymunk.Body.STATIC)
    pivot.position = pivot_pos
    joint = pymunk.PinJoint(beam, pivot)
    space.add(beam, shape, joint)
    return beam

def create_catapult(space, pivot_pos, arm_pos):
    arm = pymunk.Body(5, pymunk.moment_for_box(5, (120, 15)))
    arm.position = arm_pos
    shape = pymunk.Poly.create_box(arm, (120, 15))
    shape.elasticity = 0.6
    pivot = pymunk.Body(body_type=pymunk.Body.STATIC)
    pivot.position = pivot_pos
    joint = pymunk.PinJoint(arm, pivot)
    space.add(arm, shape, joint)
    return arm

# Create ground
create_static_segment(space, (50, 500), (750, 550))

# Create a rolling ball
ball = create_ball(space, (100, 450))

# Create a row of dominoes
dominoes = [create_domino(space, (x, 460)) for x in range(200, 500, 40)]

# Create a lever
lever = create_lever(space, (600, 470), (620, 460))

# Create a catapult
catapult = create_catapult(space, (700, 450), (710, 440))

running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    space.step(1 / FPS)
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
