"""
This program is a demonstration of platformer video game concept in which the player must reach the top of the level by bouncing off of fish.
Different types of fish give the player abilities when bouncing off of them.
This game is made for a new retro video game arcade in Lausanne.

Stephan Tinel
"""

import pygame, sys
from settings import *
from level import Level


# creating default variables
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(map, screen)


# allows program to quit
# creates a background
# loops update functions
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    background_path = "graphics/background/over_background.png"
    background = pygame.image.load(background_path)
    screen.blit(background, (0, 0))
    level.run(screen)
    pygame.display.update()
    clock.tick(fps)
