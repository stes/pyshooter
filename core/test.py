
from entities import *
import os
import pygame
import sys

pygame.init()

size = width, height = 800, 600
speed = [1, 1]
white = 0xff, 0xff, 0xff

screen = pygame.display.set_mode(size)

tank = Tank(100, 100, pygame.image.load("tank1.gif").convert_alpha(), pygame.image.load("tank1_top.gif").convert_alpha())
img = pygame.image.load('dirt.jpg')
img = pygame.transform.scale(img, (800, 600))

world = []
world.append(tank)

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
            elif event.key == pygame.K_n:
                tank.rotate_foo(math.pi/16)
            elif event.key == pygame.K_m:
                tank.rotate_foo(-math.pi/16)
            elif event.key == pygame.K_b:
                missile = tank.shoot()
                print missile
                world.append(missile)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                tank.accelerate(0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                tank.rotate(0)
                
    screen.fill(white)
    screen.blit(img, img.get_rect())
    for entity in world:
        if not entity.move():
            world.remove(entity)
        else:
            entity.render(screen)
    pygame.display.flip()
    pygame.time.wait(10)
