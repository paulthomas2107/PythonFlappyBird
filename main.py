import pygame, sys

pygame.init()
screen = pygame.display.set_mode((576, 1024))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
