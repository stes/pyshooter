'''
Created on 23.11.2012

@author: Steffen
'''
import math
import tools
import pygame

class Entity():
    
    def __init__(self, x, y, img):
        self.location = [x, y]
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0
        self.turn_velocity = 0
        self.turn_acceleration = 0
        self.img = img
        self.bufimg = self.img
        self.bufrect = self.bufimg.get_rect()
        self.max_speed = 3
        self.max_turn_speed = 0.01 * math.pi
        self.map_rect = pygame.Rect(0, 0, 800, 600)
    
    def accelerate(self, a):
        self.acceleration = a
    
    def rotate(self, a):
        self.turn_acceleration = a
    def set_angle(self, angle):
        self.angle = angle
        self.bufimg, self.bufrect = tools.rot_center(self.img, self.img.get_rect(), self.angle * 180 / math.pi)
    
    def move(self):
        old_location = self.location[:]
        
        if self.turn_acceleration != 0:
            self.turn_velocity = max(min(self.turn_velocity + self.turn_acceleration, self.max_turn_speed), -self.max_turn_speed)
        elif self.turn_velocity > 0:
            self.turn_velocity = max(self.turn_velocity - 0.0005 * math.pi, 0)
        elif self.turn_velocity < 0:
            self.turn_velocity = min(self.turn_velocity + 0.0005 * math.pi, 0)
        if self.turn_velocity != 0:
            self.set_angle(self.angle + self.turn_velocity)
        
        if self.acceleration != 0:
            mult = 3
            if self.velocity * self.acceleration > 0: mult = 1
            self.velocity = max(min(self.velocity + self.acceleration * mult, self.max_speed), -self.max_speed)
        elif self.velocity > 0:
            self.velocity = max(self.velocity - 0.2, 0)
        elif self.velocity < 0:
            self.velocity = min(self.velocity + 0.2, 0)
        self.location[0] -= math.sin(self.angle) * self.velocity
        self.location[1] -= math.cos(self.angle) * self.velocity
        
        if not self.map_rect.contains(pygame.Rect(self.location[0]-self.bufrect[2]/2, self.location[1]-self.bufrect[3]/2, self.bufrect[2], self.bufrect[3])):
            self.location = old_location[:]
        return True
    
    def render(self, display):
        display.blit(self.bufimg, [self.location[i] - self.bufrect[i+2]/2 for i in [0, 1]])
    
    def get_radius(self):
        return (self.img.get_rect()[2] + self.img.get_rect()[3]) / 2
    
    def collide(self, x, y):
        return self.get_radius(self)**2 > (self.location[0] - x)**2 + (self.location[1] - y)**2

    def alive(self):
        return True

class Tank(Entity):
    
    def __init__(self, x, y, img, top_img):
        Entity.__init__(self, x, y, img)
        self.aim_direction = 0
        self.ammo = 0
        self.health = 100
        self.top_img = top_img
        self.top_bufimg = top_img
        self.top_bufrect = top_img.get_rect()
    
    def rotate_foo(self, angle):
        self.aim_direction += angle
        self.top_bufimg, self.top_bufrect = tools.rot_center(self.top_img, self.top_img.get_rect(), self.aim_direction * 180 / math.pi)
    
    def render(self, display):
        Entity.render(self, display)
        rect = self.top_bufrect
        display.blit(self.top_bufimg, [self.location[i] - rect[i+2]/2 for i in [0, 1]])

    def shoot(self):
        x, y = (self.location[0] - math.sin(self.aim_direction) * (1+self.velocity) * 10),\
                (self.location[1] - math.cos(self.aim_direction) * (1+self.velocity) * 10)
        missile = Missile(x, y, pygame.image.load("missile.gif"), self)
        return missile

class Missile(Entity):
    
    def __init__(self, x, y, img, owner):
        Entity.__init__(self, x, y, img)
        self.velocity = 10
        self.owner = owner
        self.set_angle(owner.aim_direction)
        self.ttl = 20
    
    def alive(self):
        return (self.ttl > 0)
    
    def move(self):
        Entity.move(self)
        self.ttl -= 1
        return self.alive()

class Base(Entity):
    
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        