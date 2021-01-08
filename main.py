import pygame
import sys


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


# Set Up
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

# Game variables
gravity = 0.25
bird_movement = 0


bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(100, 512))

while True:

    # Main loop !
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Make a jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12

    # Background and floor surface
    screen.blit(bg_surface, (0, 0))

    # Bird gravity and movement
    bird_movement += gravity
    bird_rect.centery += bird_movement

    screen.blit(bird_surface, bird_rect)

    # Move floor to left
    floor_x_pos -= 1
    draw_floor()
    # Check to keep floor constant
    if floor_x_pos <= -576:
        floor_x_pos = 0

    screen.blit(floor_surface, (floor_x_pos, 900))

    pygame.display.update()
    # Frames per second refresh
    clock.tick(120)
