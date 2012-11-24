from entities import Tank, Missile, Base
from particlesys import ParticleSystem
import pygame
import sys

WIDTH = 800
HEIGHT = 600
psys = ParticleSystem()
KEY_BINDINGS_1 = {pygame.K_LEFT: "left",
                pygame.K_RIGHT: "right",
                pygame.K_UP: "up",
                pygame.K_DOWN: "down",
                pygame.K_KP1: "gun_left",
                pygame.K_KP3: "gun_right",
                pygame.K_KP2: "gun_fire"}
KEY_BINDINGS_2 = {pygame.K_a: "left",
                pygame.K_d: "right",
                pygame.K_w: "up",
                pygame.K_s: "down",
                pygame.K_g: "gun_left",
                pygame.K_j: "gun_right",
                pygame.K_h: "gun_fire"}

input_listener = []

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
    for i in range(tank2.ammo):
        screen.blit(missile, [480-missile_rect[2]*i*2, 20])
    
    missile_rect = missile.get_rect()
    for i in range(tank1.ammo):
        screen.blit(missile, [WIDTH - missile_rect[2]*i*2, HEIGHT-40])
    
    pygame.draw.rect(screen, pygame.Color(128, 0, 0), (10, 25, 200, 20), 2)
    pygame.draw.rect(screen, pygame.Color(128, 0, 0), (10, 25, tank2.health*200/Tank.MAX_HEALTH, 20))
    
    pygame.draw.rect(screen, pygame.Color(0, 128, 0), (10, 10, 200, 10), 2)
    pygame.draw.rect(screen, pygame.Color(0, 128, 0), (10, 10, tank2.shoot_reload*200/Tank.RELOAD_TIME, 10))

    
    pygame.draw.rect(screen, pygame.Color(128, 0, 0), (310, 565, 200, 20), 2)
    pygame.draw.rect(screen, pygame.Color(128, 0, 0), (310, 565, tank1.health*200/Tank.MAX_HEALTH, 20))
    
    pygame.draw.rect(screen, pygame.Color(0, 128, 0), (310, 550, 200, 10), 2)
    pygame.draw.rect(screen, pygame.Color(0, 128, 0), (310, 550, tank1.shoot_reload*200/Tank.RELOAD_TIME, 10))
        

def game_loop(tank1, tank2, world):
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                for listener in input_listener:
                    listener.on_input(event.key, event.type == pygame.KEYDOWN)
        
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
    
    tank1 = Tank(100, 500, pygame.image.load("tank1.gif"), pygame.image.load("tank1_top.gif"), KEY_BINDINGS_1)
    tank2 = Tank(700, 100, pygame.image.load("tank2.gif"), pygame.image.load("tank2_top.gif"), KEY_BINDINGS_2)
    
    input_listener.append(tank1)
    input_listener.append(tank2)
    
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
    tank1.set_world(world)
    tank2.set_world(world)
    game_loop(tank1, tank2, world)
