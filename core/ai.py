'''
Created on 25.11.2012

@author: Steffen
'''

import pygame
from entities import Tank, Base, Entity
import math

last_error = 90
actions = ["gun_right", "gun_left"]
last_action = 0
wait = 2
direction = 1
last_diff = 0

#         P  I  D
error =  [0, 0, 0]
params = [10, 0, 1]

def angle_between(tank1, tank2):
    [dx, dy] = [tank2.location[i] - tank1.location[i] for i in [0,1]]
    g = tank1.aim_direction
    [bx, by] = [-math.sin(g), -math.cos(g)]
    
    site = bx*dy - by*dx
    site /= math.fabs(site)
    
    [x, y] = tank1.location
    
    angle = math.acos((dx*bx + dy*by) / (math.hypot(dx, dy) * math.hypot(bx, by)))
    return (angle, site)

def distance_to_gunline(tank1, tank2):
    [x1, y1] = tank1.location
    [x2, y2] = tank2.location
    g = tank2.aim_direction
    [xg, yg] = [-math.sin(g), -math.cos(g)]
    
    d = -yg * (x2 - x1) + xg * (y2 - y1)
    return d

def pid(current_error, params):
    global error, last_error
        # P
    error[0] = current_error
    # I
    error[1] += error[0]
    # D
    error[2] = last_error - error[0]
    
    #print error
    
    last_error = error[0]
    return sum([error[i] * params[i] for i in range(3)])
    
def perform_action(tank, opponent, world, screen):
    global last_error, actions, last_action, wait, direction

    angle, site = angle_between(tank, opponent)
    direction = pid(angle*site, params)
    print distance_to_gunline(tank, opponent)
    if direction < 0:
        tank.perform_action(aim = 1)
    else:
        tank.perform_action(aim = -1)