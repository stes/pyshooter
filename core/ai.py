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

def perform_action(tank, opponent, world, screen):
    global last_error, actions, last_action, wait
    opponent.perform_action("down", 1)
    [dx, dy] = [opponent.location[i] - tank.location[i] for i in [0,1]]

    angle = -math.pi/2 - math.atan2(dy, dx)
    g = tank.aim_direction
    [bx, by] = [-math.sin(g), -math.cos(g)]
    
    [x, y] = tank.location
    
    pygame.draw.line(screen, (128, 0, 0), [x, y], [x+100*dx, y+100*dy])
    pygame.draw.line(screen, (0, 128, 0), [x, y], [x+100*bx, y+100*by])
        
    error = math.acos((dx*bx + dy*by) / (math.hypot(dx, dy) * math.hypot(bx, by)))
    
    diff = last_error - error;
    print error
    
    last_error = error