
from entities import *
import entities
import os
import pygame
import sys
from particlesys import ParticleSystem

WIDTH = 800
HEIGHT = 600
psys = ParticleSystem()
KEY_BINDINGS_1 = {"left": pygame.K_LEFT,
                "right" : pygame.K_RIGHT,
                "up" : pygame.K_UP,
                "down": pygame.K_DOWN,
                "gun_left": pygame.K_KP1,
                "gun_right": pygame.K_KP3,
                "gun_fire": pygame.K_KP2}
KEY_BINDINGS_2 ={"left": pygame.K_a,
                "right" : pygame.K_d,
                "up" : pygame.K_w,
                "down": pygame.K_s,
                "gun_left": pygame.K_g,
                "gun_right": pygame.K_j,
                "gun_fire": pygame.K_h}
KEY_BINDINGS = [KEY_BINDINGS_1, KEY_BINDINGS_2]

def key(action, tank):
    return KEY_BINDINGS[tank][action]

def check_collisions(world, entity):
    for p, e1 in world:
        if e1 != entity and e1.collide_entities(entity):
            if isinstance(e1, Tank):
                if isinstance(entity, Missile):
                    e1.damage(entity)
                    psys.explosion(entity.location[0], entity.location[1], 200)
                if isinstance(entity, Tank):
                    entity.step_back()
                    e1.step_back()

def render_gui(screen):
    pygame.draw.rect(screen, pygame.Color(0x44, 0x44, 0x44), (0, 0, 500, 60))
    pygame.draw.rect(screen, pygame.Color(0x44, 0x44, 0x44), (300, 540, 500, 60))
    
    missile = pygame.image.load("missile.gif")
    
    missile_rect = missile.get_rect()
    for i in range(tank1.ammo):
        screen.blit(missile, [480-missile_rect[2]*i*2, 20])
    
    missile_rect = missile.get_rect()
    for i in range(tank2.ammo):
        screen.blit(missile, [WIDTH - missile_rect[2]*i*2, HEIGHT-40])
    
    pygame.draw.rect(screen, pygame.Color(128, 0, 0), (10, 25, 200, 20), 2)
    pygame.draw.rect(screen, pygame.Color(128, 0, 0), (10, 25, tank2.health*200/entities.HEALTH, 20))
    
    pygame.draw.rect(screen, pygame.Color(128, 0, 0), (310, 565, 200, 20), 2)
    pygame.draw.rect(screen, pygame.Color(128, 0, 0), (310, 565, tank1.health*200/entities.HEALTH, 20))
    
def process_keyevent(event, tank1, tank2):
    k = event.key
    pl = 0 if k in KEY_BINDINGS_1.values() else 1
    tank = tank1 if pl==0 else tank2
    if (event.type == pygame.KEYDOWN):
        if k == key("left", pl): tank.rotate(+math.pi/6000)
        elif k == key("right", pl): tank.rotate(-math.pi/6000)
        elif k == key("up", pl): tank.accelerate(0.05)
        elif k == key("down", pl): tank.accelerate(-0.05)
        elif k == key("gun_left", pl): tank.acc_rotation(+math.pi/2000)
        elif k == key("gun_right", pl): tank.acc_rotation(-math.pi/2000)
        elif k == key("gun_fire", pl):
            missile = tank.shoot()
            if missile != None:
                world.append([missile.priority, missile])
    elif event.type == pygame.KEYUP:
        if event.key == key("up", pl) or event.key == key("down", pl):
            tank.accelerate(0)
        elif event.key == key("right", pl) or event.key == key("left", pl):
            tank.rotate(0)
        elif event.key == key("gun_right", pl) or event.key == key("gun_left", pl):
            tank.acc_rotation(0)
        

def game_loop(tank1, tank2, world):
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                process_keyevent(event, tank1, tank2)
                    
        screen.fill(white)
        screen.blit(img, img.get_rect())
        world.sort()
        for [p, entity] in world:
            if not entity.move():
                world.remove([entity.priority, entity])
            else:
                check_collisions(world, entity)
                entity.render(screen)
        
        psys.tick()
        psys.render(screen)
        
        render_gui(screen)
        
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    pygame.init()
    
    size = width, height = WIDTH, HEIGHT
    white = 0xff, 0xff, 0xff
    
    screen = pygame.display.set_mode(size)
    
    tank1 = Tank(100, 500, pygame.image.load("tank1.gif"), pygame.image.load("tank1_top.gif"))
    tank2 = Tank(700, 100, pygame.image.load("tank2.gif"), pygame.image.load("tank2_top.gif"))
    
    base1 = Base(100, 500, pygame.image.load("base.gif"), tank1)
    base2 = Base(700, 100, pygame.image.load("base.gif"), tank2)
    
    img = pygame.image.load('dirt.jpg')
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
    
    world = []
    world.append(base1)
    world.append(base2)
    world.append(tank1)
    world.append(tank2)
    world = [[e.priority, e] for e in world]
    game_loop(tank1, tank2, world)
    
    
