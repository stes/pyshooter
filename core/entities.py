'''
Created on 23.11.2012

@author: Steffen
'''
import pygame, math, tools

class Entity():
    
    def __init__(self, x, y, img):
        self.location = [x, y]
        self.angle = 0
        self.velocity = 0
        self.img = img
        self.bufimg = self.img
        self.bufrect = self.bufimg.get_rect()
    
    def accelerate(self, a):
        self.velocity += a
    
    def rotate(self, rad):
        self.set_angle(self.angle + rad)
    
    def set_angle(self, angle):
        self.angle = angle
        self.bufimg, self.bufrect = tools.rot_center(self.img, self.img.get_rect(), self.angle * 180 / math.pi)
    
    def move(self):
        self.location[0] -= math.sin(self.angle) * self.velocity
        self.location[1] -= math.cos(self.angle) * self.velocity
        return True
    
    def render(self, display):
        rect = self.bufrect
        display.blit(self.bufimg, [self.location[i] - rect[i+2]/2 for i in [0, 1]])
    
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
        