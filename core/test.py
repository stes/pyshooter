
from entities import *
import os
import pygame
import sys

def check_collisions(world, entity):
    for e1 in world:
        if e1 != entity and e1.collide_entities(entity):
            if isinstance(e1, Tank):
                if isinstance(entity, Missile):
                    e1.damage(entity)
                if isinstance(entity, Tank):
                    entity.step_back()
                    e1.step_back()
                

if __name__ == '__main__':
    pygame.init()
    
    size = width, height = 800, 600
    white = 0xff, 0xff, 0xff
    
    screen = pygame.display.set_mode(size)
    
    tank1 = Tank(100, 100, pygame.image.load("tank1.gif").convert_alpha(), pygame.image.load("tank1_top.gif").convert_alpha())
    tank2 = Tank(500, 100, pygame.image.load("tank2.gif").convert_alpha(), pygame.image.load("tank2_top.gif").convert_alpha())
    
    img = pygame.image.load('dirt.jpg')
    img = pygame.transform.scale(img, (800, 600))
    
    world = []
    world.append(tank1)
    world.append(tank2)
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tank1.rotate(+math.pi/6000)
                elif event.key == pygame.K_RIGHT:
                    tank1.rotate(-math.pi/6000)
                elif event.key == pygame.K_UP:
                    tank1.accelerate(0.05)
                elif event.key == pygame.K_DOWN:
                    tank1.accelerate(-0.05)
                elif event.key == pygame.K_n:
                    tank1.acc_rotation(+math.pi/2000)
                elif event.key == pygame.K_m:
                    tank1.acc_rotation(-math.pi/2000)
                elif event.key == pygame.K_b:
                    missile = tank1.shoot()
                    if missile != None:
                        world.append(missile)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    tank1.accelerate(0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    tank1.rotate(0)
                elif event.key == pygame.K_m or event.key == pygame.K_n:
                    tank1.acc_rotation(0)
                    
        screen.fill(white)
        screen.blit(img, img.get_rect())
        for entity in world:
            if not entity.move():
                world.remove(entity)
            else:
                check_collisions(world, entity)
                entity.render(screen)
        pygame.display.flip()
        pygame.time.wait(10)
