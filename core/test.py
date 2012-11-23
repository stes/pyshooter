
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
tank2 = Entity(300, 300, pygame.image.load("tank2.gif").convert_alpha())


objects = [tank, tank2]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tank.rotate(+math.pi/6000)
            elif event.key == pygame.K_RIGHT:
                tank.rotate(-math.pi/6000)
            elif event.key == pygame.K_UP:
                tank.accelerate(0.05)
            elif event.key == pygame.K_DOWN:
                tank.accelerate(-0.05)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                tank.accelerate(0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                tank.rotate(0)
    tank.move()
    screen.fill(white)
    for obj in objects:
        obj.render(screen)
    pygame.display.flip()
    pygame.time.wait(10)
