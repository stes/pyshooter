'''
Created on 25.11.2012

@author: Steffen
'''

import pygame
import entities
from entities import Tank, Base, Entity, Missile
import math
#import numpy
import random
import main
import copy
import tools
from vector import Vector2D

class AntiGravity():
    
    def wall_error(self, x, y):
        Ex = 1 / x**2 - 1 / math.fabs((x - main.WIDTH) ** 2)
        Ex *= main.WIDTH**2
        Ey = 1 / y**2 - 1 / math.fabs((y - main.HEIGHT) ** 2)
        Ey *= main.HEIGHT**2
        return Vector2D(Ex, Ey)
        
    def point_error(self, location, p, force):
        [x, y] = location.list()
        e = force / (math.hypot((x - p.x),(y - p.y)) ** 2)
        return Vector2D((x-p.x) * e, (y-p.y)*e)
    
    def continious_gradient(self, location, p, force):
        [x, y] = location.list()
        e = force / (math.hypot((x - p.x),(y - p.y)))
        return Vector2D((x-p.x) * e, (y-p.y)*e)
    
    def add_gravity_point(self, x, y, force):
        self.gravity_points.append([x, y, force])

class PIDControl():
    
    def __init__(self, params):
        self.error = [0., 0., 0.]
        self.params = params
        self.last_error = 0.
        self.current_error = 0.
    
    def pid(self, current_error):
        # P
        self.error[0] = current_error
        # I
        self.error[1] += self.error[0]
        # D
        self.error[2] = self.last_error - self.error[0]
        
        self.last_error = self.error[0]
        return sum([self.error[i] * self.params[i] for i in range(3)])

#wait = 2
#direction = 1
#last_diff = 0
#observations = []
#targets = []
#model = neural.Model(20,10,10)
rnd = random.Random()
actions = [[0, 0],
           [0, 1],
           [1, 0]]

def angle_between(tank1, tank2):
    diff = tank2.location - tank1.location
    g = tank1.aim_direction
    b = Vector2D(-math.sin(g), -math.cos(g))
    
    s = site(diff, b)
    
    a = angle(diff, b)
    return (a, s)

def site(a, b):
    return tools.sign(a.cross(b))

def angle(a, b, abs=False):
    dot = a.dot(b)
    if abs: dot=math.fabs(dot)
    return math.acos((dot) /
              (math.hypot(a.x, a.y) * math.hypot(b.x, b.y)))

def world_repr(tank, opponent, world):
    rep = []
    rep.extend(tank.get_repr())
    rep.extend(opponent.get_repr())
    a, s = angle_between(tank, opponent)
    rep.append(a*s)
    a, s = angle_between(opponent, tank)
    rep.append(a*s)
    return rep

def distance_to_line(a, b, g):
    #[x1, y1] = a
    #[x2, y2] = b
    g = Vector2D(-math.sin(g), -math.cos(g))
    #d = -yg * (x2 - x1) + xg * (y2 - y1)
    #xf = [-yg * d, xg * d]
    
    d, xf = a.projection(b, g)
    
    return [math.fabs(d), xf]
    
def observe(tank, opponent, world, screen):
    pass
#    global last_error, actions, last_action, wait, direction, model, observations, targets
#    return
#    angle, site = angle_between(tank, opponent)
#    direction = pid(angle*site, params)
    #print distance_to_gunline(tank, opponent)
#    if direction < 0:
#        tank.perform_action(aim = 1)
#    else:
#        tank.perform_action(aim = -1)
#    r = world_repr(tank, opponent, world)
#    observations.append(r)
#    targets.append(expand_targets(tank.last_action))
#    if len(observations) > 100:
#        print 'performing an update'
#        X = numpy.array(observations)
#        Y = numpy.array(targets)
#        for i in range(10):
#            grad1, grad2 = model.gradients(X, Y)
#            model.update(grad1, grad2, 0.05)
#        observations = []
#        targets = []
    #print "  ".join([str(int(r[i] * 100)/100.) for i in range(len(r))])

def expand_targets(t):
    return [t[0],
             t[1],
             t[0] == t[1],
             t[2],
             t[3],
             t[2] == t[3],
             t[4],
             t[5],
             t[4] == t[5],
             t[6]]

#def perform_action(tank, opponent, world):
#    r = world_repr(tank, opponent, world)
#    X = numpy.array(r)
#    h, y = model.compute(X)
#    tank.perform_action(sample(y))

def sample(x):
    global rnd
    actions = [0, 0, 0, 0, 0, 0]
    shoot = int(rnd.random() < x[9])
    probs = [math.exp(x[i]) for i in range(9)]
    for i in range(3):
        s = 0.
        for j in range(3):
            s += probs[i*3+j]
        actions[i*2] = int(rnd.random() < probs[i*3]/s)
        actions[i*2+1] = int(rnd.random() < probs[i*3+1]/s)
    actions.append(shoot)
    return actions

class RandomBot(Tank):
    
    def __init__(self, x, y, img, top_img, key_binding=None):
        Tank.__init__(self, x, y, img, top_img, key_binding)
        self.pid_aim = PIDControl([10., 0., 1.])
    
    def action(self, opponent, world):
        a, s = angle_between(self, opponent)
        aim = [0, 0]
        if self.pid_aim.pid(a*s) < 0: aim = [1, 0]
        else: aim = [0, 1]
        
        turn = [rnd(0.50), rnd(0.25)]
        move = [0, 1]
        shoot = [0]
        
        best_action = move + turn + aim + shoot
        self.perform_action(best_action)

def rnd(prob):
    return int(random.random() <= prob)


class AIBot(Tank):
    
    def __init__(self, x, y, img, top_img, key_binding=None):
        Tank.__init__(self, x, y, img, top_img, key_binding)
        self.pid_aim = PIDControl([10., 0., 1.])
        self.pid_turn = PIDControl([20., 0., 0.])
        self.anti_gravity = AntiGravity()
    
    def action(self, opponent, world):
        global actions, wait, direction, model, observations, targets, pid_aim, pid_move, pid_turn
        a, s = angle_between(self, opponent)
        aim = tools.sign(-self.pid_aim.pid(a*s))
        
        g = self.compute_error(opponent, world)
        
        if g.x == 0 and g.y == 0:
            return
        
#        [x, y] = self.location[:]
#        [x0, y0] = [x+10*g[0], y+10*g[1]]
#        pygame.draw.line(main.screen, pygame.Color(0, 128, 0), (x,y), (x0,y0), 5)
        
        a = Vector2D(-math.sin(self.angle),-math.cos(self.angle))
#        [x1, y1] = [x+100*a[0], y+100*a[1]]
#        pygame.draw.line(main.screen, pygame.Color(0, 0, 128), (x,y), (x1,y1), 5)
        
        r = angle(a, g)
        s = site(a, g)
        
        turn = tools.sign(self.pid_turn.pid(min(r, math.fabs(math.pi-r))*s))
        move = tools.sign(math.pi/2 - r)
        shoot = r < math.pi/16
    
        self.perform_action(move, turn, aim, shoot)
        
        print self.location

    def missile_error(self, world):
        error = Vector2D()
        for entity in world:
            if isinstance(entity, Missile) and entity.owner != self:
                [d, dv] = distance_to_line(self.location, entity.location, entity.angle)
                xf = self.location + dv
                error += self.anti_gravity.point_error(self.location, xf, 50000)
                #pygame.draw.rect(main.screen, pygame.Color(200,0,0),(xf.x,xf.y,20,20))
        return error

    def compute_error(self, opponent, world):
        x, y = self.location.x, self.location.y
        d, dv = distance_to_line(self.location, opponent.location, opponent.aim_direction)
        xf = self.location + dv
        #pygame.draw.rect(main.screen, pygame.Color(0,128,0),(xf.x,xf.y,10,10))
        g = self.anti_gravity.wall_error(x, y)
        
        # avoid gunline
        r, s = angle_between(opponent, self)
        gunline_error = Vector2D(0,0)
        if r < math.pi/2:
            gunline_error = self.anti_gravity.point_error(self.location, xf, 10000)
        
        # avoid missiles
        m_error = self.missile_error(world)
        
        # go to base
        g_base = Vector2D(0, 0)
        if self.location.x != self.base.location.x or self.location.y != self.base.location.y:
            g_base = self.anti_gravity.continious_gradient(self.location, self.base.location, -1000/(0.1+self.ammo**2))
        
        g += gunline_error + m_error + g_base
        return g