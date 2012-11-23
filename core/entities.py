'''
Created on 23.11.2012

@author: Steffen
'''

class Entity():
    
    def __init__(self, x, y, img):
        self.location = [x, y]
        self.velocity = [0, 0]
        self.img = img
    
    def accelerate(self, ddx, ddy):
        self.velocity[0] += ddx
        self.velocity[1] += ddy
        
    def move(self):
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
    
    def render(self, display):
        display.blit(self.img, self.location)

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
        