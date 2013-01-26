'''
Created on 23.11.2012

This file contains the entities involved in the game. All entities use
the base class implementation 'Entity'.
'''
import math
import tools
import pygame
from vector import Vector2D

game_map = pygame.Rect(0, 0, 800, 600)

class Entity():
    
    def __init__(self, x, y, img, priority):
        #
        # ADD CODE HERE
        #
        self.img = img
        self.bufimg = self.img
        if self.bufimg != None: self.bufrect = self.bufimg.get_rect()
        self.map_rect = game_map
    
    def set_angle(self, angle):
        self.angle = angle
        if self.bufimg != None:
            # rotate image
            self.bufimg, self.bufrect = tools.rot_center(self.img, self.img.get_rect(), self.angle * 180 / math.pi)
            
    def render(self, display):
        display.blit(self.bufimg, [self.location[i] - self.bufrect[i+2]/2 for i in [0, 1]])
    
    def alive(self):
        return True
    
    def tick(self):
        pass
        #
        # ADD CODE HERE
        #
    
    def get_radius(self):
        pass
        #
        # ADD CODE HERE
        #
    
    def collide(self, vector):
        pass
        #
        # ADD CODE HERE
        #
    
    def collide_entities(self, other):
        pass
        #
        # ADD CODE HERE
        #

class Tank(Entity):
    # some constants
    MAX_AMMO = 10
    MAX_HEALTH = 100
    RELOAD_TIME = 100
    #
    # Add some more constants!
    #
    # ADD CODE HERE
    #
    
    def __init__(self, x, y, img, top_img, key_binding):
        Entity.__init__(self, x, y, img, 10)
        #
        # ADD CODE HERE
        #
        self.top_img = top_img
        self.top_bufimg = top_img
        if self.top_bufimg != None: self.top_bufrect = top_img.get_rect()
        self.old_location = self.location
        self.key_binding = key_binding
        self.last_action = [0, 0, 0]
    
    def set_base(self, base):
        self.base = base
    
    def ready_to_shoot(self):
        return self.shoot_reload == Tank.RELOAD_TIME and self.ammo > 0
    
    def step_back(self):
        self.location = self.old_location.copy()
    
    def to_base(self, b):
        if b.owner == self:
            self.ammo = Tank.MAX_AMMO
    
    def decelerate(self, acc, vel, dec, limit, mult=1):
        if acc != 0:
            vel = max(min(vel + acc*dec*mult, limit), -limit)
        elif vel > 0:
            vel = max(vel - dec, 0)
        elif vel < 0:
            vel = min(vel + dec, 0)
        return vel
    
    def render(self, display):
        Entity.render(self, display)
        rect = self.top_bufrect
        display.blit(self.top_bufimg, [self.location.list()[i] - rect[i+2]/2 for i in [0, 1]])
        
    def set_world(self, world):
        self.world = world
    
    def on_input(self, keys):
        # TODO improve this
        actions = []
        for key in keys:
            if key in self.key_binding.keys():
                actions.append(self.key_binding[key])
        #
        self.last_action = [int("up" in actions),
                            int("down" in actions),
                            int("left" in actions),
                            int("right" in actions),
                            int("gun_left" in actions),
                            int("gun_right" in actions),
                            int("gun_fire" in actions)]
        self.perform_action(self.last_action)
    
    def perform_action_move(self, move=0, turn=0, aim=0):
        self.acceleration = int(move)
        self.turn_acceleration = int(turn)
        self.aim_acceleration = int(aim)
        
    def shoot(self):
        if self.ready_to_shoot():
            safe_dist = Vector2D(math.sin(self.aim_direction) * 40,
                                 math.cos(self.aim_direction) * 40)
            
            start_pos = self.location - safe_dist
            #
            # ADD CODE HERE
            #
    
    def tick(self):
        # save copy of old location
        self.old_location = self.location.copy()
        
        # update velocities
        #
        # ADD CODE HERE
        #
        
        # update positions
        #
        # ADD CODE HERE
        #
        
        # check if position is valid
        #
        # ADD CODE HERE
        #       
        
        # reload the gun
        #
        # ADD CODE HERE
        #        
    
    def check_borders(self):
        pass
        #
        # ADD CODE HERE
        #
    
    def rotate_gun_to(self, angle):
        pass
        #
        # ADD CODE HERE
        #
    
    def damage(self, missile):
        pass
        #
        # ADD CODE HERE
        #
    
    def alive(self):
        pass
        #
        # ADD CODE HERE
        #
    
    def perform_action(self, actions):
        pass
        #
        # ADD CODE HERE
        #
                
                    
class Missile(Entity):
    
    def __init__(self, x, y, img, owner):
        pass
        #
        # ADD CODE HERE
        #
    
    # Implement the methods "destroy", "alive" and "move"
    #
    # ADD CODE HERE
    #


class Base(Entity):
    
    # implement the constructor!
    #
    # ADD CODE HERE
    #
    
    def tick(self):
        if self.owner.collide_entities(self) and self.preparation_time == 0:
            while (self.owner.ammo < 10):
                self.preparation_time += 50
                self.owner.ammo += 1
        self.preparation_time = max(self.preparation_time - 1, 0)
        