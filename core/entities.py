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
        self.angle += rad
        self.bufimg, self.bufrect = tools.rot_center(self.img, self.img.get_rect(), self.angle * 180 / math.pi)
    
    def move(self):
        self.location[0] -= math.sin(self.angle) * self.velocity
        self.location[1] -= math.cos(self.angle) * self.velocity
    
    def render(self, display):
        rect = self.bufrect
        display.blit(self.bufimg, [self.location[i] + rect[i] for i in [0, 1]])

class Tank(Entity):
    
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.direction = 0
        self.ammo = 0
        self.health = 100

class Missile(Entity):
    
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        pass

class Base(Entity):
    
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        