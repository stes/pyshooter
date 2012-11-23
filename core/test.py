
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
                if isinstance(entity, Base):
                    e1.to_base(entity)
                

if __name__ == '__main__':
    pygame.init()
    
    size = width, height = 800, 600
    white = 0xff, 0xff, 0xff
    
    screen = pygame.display.set_mode(size)
    
    tank1 = Tank(100, 500, pygame.image.load("tank1.gif"), pygame.image.load("tank1_top.gif"))
    tank2 = Tank(700, 100, pygame.image.load("tank2.gif"), pygame.image.load("tank2_top.gif"))
    
    base1 = Base(100, 500, pygame.image.load("base.gif"), tank1)
    base2 = Base(700, 100, pygame.image.load("base.gif"), tank2)
    
    img = pygame.image.load('dirt.jpg')
    img = pygame.transform.scale(img, (800, 600))
    
    world = []
    world.append(base1)
    world.append(base2)
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
                elif event.key == pygame.K_a:
                    tank2.rotate(+math.pi/6000)
                elif event.key == pygame.K_d:
                    tank2.rotate(-math.pi/6000)
                elif event.key == pygame.K_w:
                    tank2.accelerate(0.05)
                elif event.key == pygame.K_s:
                    tank2.accelerate(-0.05)
                elif event.key == pygame.K_g:
                    tank2.acc_rotation(+math.pi/2000)
                elif event.key == pygame.K_h:
                    tank2.acc_rotation(-math.pi/2000)
                elif event.key == pygame.K_j:
                    missile = tank2.shoot()
                    if missile != None:
                        world.append(missile)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    tank1.accelerate(0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    tank1.rotate(0)
                elif event.key == pygame.K_m or event.key == pygame.K_n:
                    tank1.acc_rotation(0)
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    tank2.accelerate(0)
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    tank2.rotate(0)
                elif event.key == pygame.K_g or event.key == pygame.K_h:
                    tank2.acc_rotation(0)
                    
        screen.fill(white)
        screen.blit(img, img.get_rect())
        for entity in world:
            if not entity.move():
                world.remove(entity)
            else:
                check_collisions(world, entity)
                entity.render(screen)
        
            pygame.draw.rect(screen, pygame.Color(0x44, 0x44, 0x44), (0, 0, 500, 60))
        pygame.draw.rect(screen, pygame.Color(0x44, 0x44, 0x44), (300, 540, 500, 60))
        
        missile = pygame.image.load("missile.gif")
        
        missile_rect = missile.get_rect()
        for i in range(tank1.ammo):
            screen.blit(missile, [10+missile_rect[2]*i*2, 10])
        
        missile_rect = missile.get_rect()
        for i in range(tank2.ammo):
            screen.blit(missile, [310+missile_rect[2]*i*2, 550])
        
        pygame.draw.rect(screen, pygame.Color(0xff, 0, 0), (10, 25, 200, 20), 2)
        pygame.draw.rect(screen, pygame.Color(0xff, 0, 0), (10, 25, tank1.health*2, 20))
        
        pygame.draw.rect(screen, pygame.Color(0xff, 0, 0), (310, 565, 200, 20), 2)
        pygame.draw.rect(screen, pygame.Color(0xff, 0, 0), (310, 565, tank2.health*2, 20))
    
        pygame.display.flip()
        pygame.time.wait(10)
