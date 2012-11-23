
from entities import *
import os
import pygame
import sys

pygame.init()

size = width, height = 800, 600
speed = [1, 1]
white = 0xff, 0xff, 0xff

screen = pygame.display.set_mode(size)

tank = Entity(100, 100, pygame.image.load("tank1.gif").convert_alpha())

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tank.rotate(+math.pi/16)
            elif event.key == pygame.K_RIGHT:
                tank.rotate(-math.pi/16)
            elif event.key == pygame.K_UP:
                tank.accelerate(0.5)
            elif event.key == pygame.K_DOWN:
                tank.accelerate(-0.5)
    tank.move()
    screen.fill(white)
    tank.render(screen)
    pygame.display.flip()
    pygame.time.wait(10)
