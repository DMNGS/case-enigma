import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0,200,0), (100, 250), 75)
    pygame.draw.circle(screen, (0,200,0), (250, 100), 75)
    pygame.draw.circle(screen, (0,200,0), (250, 400), 75)
    pygame.draw.circle(screen, (0,200,0), (400, 250), 75)
    pygame.display.flip()
pygame.quit()