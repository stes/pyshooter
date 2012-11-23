'''
Created on 23.11.2012

@author: Steffen
'''
import math
import tools
import pygame

''' Game Constants '''

MAX_SPEED = 3
MAX_TURN_SPEED = 0.01 * math.pi
AMMO = 10
HEALTH = 100

'''                '''

class Entity():
    
    def __init__(self, x, y, img, priority):
        self.location = [x, y]
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0
        self.turn_velocity = 0
        self.turn_acceleration = 0
        self.img = img
        self.bufimg = self.img
        self.bufrect = self.bufimg.get_rect()
        self.max_speed = MAX_SPEED
        self.max_turn_speed = MAX_TURN_SPEED
        self.map_rect = pygame.Rect(0, 0, 800, 600)
        self.priority = priority
    
    def accelerate(self, a):
        self.acceleration = a
    
    def rotate(self, a):
        self.turn_acceleration = a
    
    def set_angle(self, angle):
        self.angle = angle
        self.bufimg, self.bufrect = tools.rot_center(self.img, self.img.get_rect(), self.angle * 180 / math.pi)
    
    def move(self):
        self.location[0] -= math.sin(self.angle) * self.velocity
        self.location[1] -= math.cos(self.angle) * self.velocity
        return self.alive()
    
    def render(self, display):
        display.blit(self.bufimg, [self.location[i] - self.bufrect[i+2]/2 for i in [0, 1]])
    
    def get_radius(self):
        return (self.img.get_rect()[2] + self.img.get_rect()[3]) / 2
    
    def collide(self, x, y):
        return self.get_radius()**2 > (self.location[0] - x)**2 + (self.location[1] - y)**2
    
    def collide_entities(self, other):
        return 0.3*(self.get_radius()+other.get_radius())**2 > (self.location[0] - other.location[0])**2 + (self.location[1] - other.location[1])**2

    def alive(self):
        return True

class Tank(Entity):
    
    def __init__(self, x, y, img, top_img):
        Entity.__init__(self, x, y, img, 10)
        self.aim_direction = 0
        self.ammo = AMMO
        self.health = HEALTH
        self.top_img = top_img
        self.top_bufimg = top_img
        self.top_bufrect = top_img.get_rect()
        self.aim_velocity = 0
        self.aim_acceleration = 0
        self.old_location = self.location
    
    def step_back(self):
        self.location = self.old_location[:]
    
    def to_base(self, b):
        if b.owner == self:
            self.ammo = AMMO
    
    def move(self):
        self.old_location = self.location[:]
        
        if self.turn_acceleration != 0:
            self.turn_velocity = max(min(self.turn_velocity + self.turn_acceleration, self.max_turn_speed), -self.max_turn_speed)
        elif self.turn_velocity > 0:
            self.turn_velocity = max(self.turn_velocity - 0.0005 * math.pi, 0)
        elif self.turn_velocity < 0:
            self.turn_velocity = min(self.turn_velocity + 0.0005 * math.pi, 0)
        if self.turn_velocity != 0:
            self.set_angle(self.angle + self.turn_velocity)
        
        if self.aim_acceleration != 0:
            self.aim_velocity = max(min(self.aim_velocity + self.aim_acceleration, self.max_turn_speed), -self.max_turn_speed)
        elif self.aim_velocity > 0:
            self.aim_velocity = max(self.aim_velocity - 0.005 * math.pi, 0)
        elif self.aim_velocity < 0:
            self.aim_velocity = min(self.aim_velocity + 0.005 * math.pi, 0)
        if self.aim_velocity != 0:
            self.rotate_gun_by(self.aim_velocity)
        
        if self.acceleration != 0:
            mult = 3
            if self.velocity * self.acceleration > 0:
                mult = 1
            self.velocity = max(min(self.velocity + self.acceleration * mult, self.max_speed), -self.max_speed)
        elif self.velocity > 0:
            self.velocity = max(self.velocity - 0.2, 0)
        elif self.velocity < 0:
            self.velocity = min(self.velocity + 0.2, 0)

        Entity.move(self)
        
        if not self.map_rect.contains(pygame.Rect(self.location[0]-self.bufrect[2]/2, self.location[1]-self.bufrect[3]/2, self.bufrect[2], self.bufrect[3])):
            self.step_back()
        
        return self.alive()
    
    def acc_rotation(self, acc):
        self.aim_acceleration = acc
    
    def rotate_gun_to(self, angle):
        self.aim_direction = angle
        self.top_bufimg, self.top_bufrect = tools.rot_center(self.top_img, self.top_img.get_rect(), self.aim_direction * 180 / math.pi)
    
    def rotate_gun_by(self, angle):
        self.rotate_gun_to(self.aim_direction + angle)
        
    def render(self, display):
        Entity.render(self, display)
        rect = self.top_bufrect
        display.blit(self.top_bufimg, [self.location[i] - rect[i+2]/2 for i in [0, 1]])
    
    def damage(self, missile):
        if missile.owner != self:
            self.health -= missile.damage
            missile.destroy()
    
    def alive(self):
        return self.health > 0

    def shoot(self):
        if self.ammo > 0:
            x, y = (self.location[0] - math.sin(self.aim_direction) * 40),\
                    (self.location[1] - math.cos(self.aim_direction) * 40)
            missile = Missile(x, y, pygame.image.load("missile.gif"), self)
            self.ammo -= 1
            return missile
        return None

class Missile(Entity):
    
    def __init__(self, x, y, img, owner):
        Entity.__init__(self, x, y, img, 5)
        self.velocity = 10
        self.owner = owner
        self.set_angle(owner.aim_direction)
        self.ttl = 200
        self.damage = 10
    
    def destroy(self):
        self.ttl = 0
    
    def alive(self):
        return (self.ttl > 0) and (self.velocity > 2)
    
    def move(self):
        Entity.move(self)
        self.ttl -= 1
        return self.alive()

class Base(Entity):
    
    def __init__(self, x, y, img, owner):
        Entity.__init__(self, x, y, img, 0)
        self.owner = owner
        self.preparation_time = 0
    
    def get_radius(self):
        return 10
    
    def move(self):
        if self.owner.collide_entities(self) and self.preparation_time == 0:
            while (self.owner.ammo < 10):
                self.preparation_time += 50
                self.owner.ammo += 1
        self.preparation_time = max(self.preparation_time - 1, 0)
        return True
        