'''
Created on 23.11.2012

This file contains the entities involved in the game. All entities use
the base class implementation 'Entity'.
'''
import math
import tools
import pygame

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
        self.map_rect = pygame.Rect(0, 0, 800, 600)
        self.priority = priority
    
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
    MAX_SPEED = 3
    MAX_TURN_SPEED = 0.01 * math.pi
    MAX_AMMO = 10
    MAX_HEALTH = 100
    RELOAD_TIME = 100
    
    def __init__(self, x, y, img, top_img, key_binding):
        Entity.__init__(self, x, y, img, 10)
        self.aim_direction = 0
        self.top_img = top_img
        self.top_bufimg = top_img
        self.top_bufrect = top_img.get_rect()
        self.aim_velocity = 0
        self.aim_acceleration = 0
        self.old_location = self.location
        self.shoot_reload = 0
        self.key_binding = key_binding
        self.ammo = Tank.MAX_AMMO
        self.health = Tank.MAX_HEALTH
        
    def ready_to_shoot(self):
        return self.shoot_reload == Tank.RELOAD_TIME and self.ammo > 0
    
    def step_back(self):
        self.location = self.old_location[:]
    
    def to_base(self, b):
        if b.owner == self:
            self.ammo = Tank.MAX_AMMO
    
    def move(self):
        self.old_location = self.location[:]
        
        if self.turn_acceleration != 0:
            self.turn_velocity = max(min(self.turn_velocity + self.turn_acceleration, Tank.MAX_TURN_SPEED), -Tank.MAX_TURN_SPEED)
        elif self.turn_velocity > 0:
            self.turn_velocity = max(self.turn_velocity - 0.0005 * math.pi, 0)
        elif self.turn_velocity < 0:
            self.turn_velocity = min(self.turn_velocity + 0.0005 * math.pi, 0)
        if self.turn_velocity != 0:
            self.set_angle(self.angle + self.turn_velocity)
        
        if self.aim_acceleration != 0:
            self.aim_velocity = max(min(self.aim_velocity + self.aim_acceleration, Tank.MAX_TURN_SPEED), -Tank.MAX_TURN_SPEED)
        elif self.aim_velocity > 0:
            self.aim_velocity = max(self.aim_velocity - 0.005 * math.pi, 0)
        elif self.aim_velocity < 0:
            self.aim_velocity = min(self.aim_velocity + 0.005 * math.pi, 0)
        if self.aim_velocity != 0:
            self.rotate_gun_to(self.aim_direction + self.aim_velocity)
        
        if self.acceleration != 0:
            mult = 3
            if self.velocity * self.acceleration > 0:
                mult = 1
            self.velocity = max(min(self.velocity + self.acceleration * mult, Tank.MAX_SPEED), -Tank.MAX_SPEED)
        elif self.velocity > 0:
            self.velocity = max(self.velocity - 0.2, 0)
        elif self.velocity < 0:
            self.velocity = min(self.velocity + 0.2, 0)

        Entity.move(self)
        
        for i in [0, 1]:
            if self.location[i]-self.bufrect[i+2]/2 < self.map_rect[i]:
                self.location[i] = self.map_rect[i] + self.bufrect[i+2]/2
            if self.location[i]+self.bufrect[i+2]/2 > self.map_rect[i]+self.map_rect[i+2]:
                self.location[i] = self.map_rect[i]+self.map_rect[i+2] - self.bufrect[i+2]/2
        
        self.shoot_reload = min(self.shoot_reload+1, Tank.RELOAD_TIME)
        
        return self.alive()
    
    def rotate_gun_to(self, angle):
        self.aim_direction = angle
        self.top_bufimg, self.top_bufrect = tools.rot_center(self.top_img, self.top_img.get_rect(), self.aim_direction * 180 / math.pi)
    
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
        if self.ready_to_shoot():
            x, y = (self.location[0] - math.sin(self.aim_direction) * 40),\
                    (self.location[1] - math.cos(self.aim_direction) * 40)
            missile = Missile(x, y, pygame.image.load("missile.gif"), self)
            self.ammo -= 1
            self.shoot_reload = 0
            return missile
        return None
    
    def set_world(self, world):
        self.world = world
    
    def on_input(self, key, state):
        if self.key_binding.has_key(key):
            action = self.key_binding[key]
            mult = 1 if state else -1
            if action == "left": self.turn_acceleration += math.pi/2000 * mult
            elif action == "right": self.turn_acceleration -= math.pi/2000 * mult
            elif action == "up": self.acceleration += 0.05 * mult
            elif action == "down": self.acceleration -= 0.05 * mult
            elif action == "gun_left": self.aim_acceleration += math.pi/2000 * mult
            elif action == "gun_right": self.aim_acceleration -= math.pi/2000 * mult
            elif action == "gun_fire":
                missile = self.shoot()
                if missile != None:
                    self.world.append([missile.priority, missile])

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
        