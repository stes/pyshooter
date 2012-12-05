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
    
    #pygame.draw.line(screen, (128, 0, 0), [x, y], [x+100*dx, y+100*dy])
    #pygame.draw.line(screen, (0, 128, 0), [x, y], [x+100*bx, y+100*by])
    
    angle, site = angle_between(tank, opponent)
    
    direction = pid(angle*site, params)
    #print direction

    #tank.aim_velocity = -direction * math.pi/100
    action = ''
    if direction < 0:
        action = 'gun_left'
    else:
        action = 'gun_right'