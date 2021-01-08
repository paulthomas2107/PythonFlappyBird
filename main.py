import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


# Set Up
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font()

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0


bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_down_flap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png')).convert_alpha()
bird_mid_flap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png')).convert_alpha()
bird_up_flap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png')).convert_alpha()
bird_frames = [bird_down_flap, bird_mid_flap, bird_up_flap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))
BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)
pipe_height = [400, 600, 800]


while True:
    # Main loop !
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Make a jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
        # Make a pipe
        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())
        # Bird flap movements
        if event.type == BIRD_FLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    # Background and floor surface
    screen.blit(bg_surface, (0, 0))

    # Game active check
    if game_active:
        # Bird gravity and movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        # Check any collisions
        game_active = check_collision(pipe_list)
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

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
