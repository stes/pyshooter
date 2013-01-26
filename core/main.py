'''
This is the project's main file. It contains the game loop which
handles the interaction between players in the game.

25.11.12
'''


from entities import Tank, Missile, Base
import pygame
import sys



''' General constants '''
WIDTH = 800
HEIGHT = 600
'''                    '''

''' Key bindings for both players '''
KEY_BINDINGS_1 = {pygame.K_LEFT: "left",
                pygame.K_RIGHT: "right",
                pygame.K_UP: "up",
                pygame.K_DOWN: "down",
                pygame.K_n: "gun_left",
                pygame.K_COMMA: "gun_right",
                pygame.K_m: "gun_fire"}
#
# Add key bindings for the second player
#
# ADD CODE HERE
#
'''                                '''

input_listener = []
keys_pressed = []

def check_collisions(world, entity):
    for p, e1 in world:
        if e1 != entity and e1.collide_entities(entity):
            pass
            # Tank:
            # check for collision with:
            # other tank, missile (-> explosion)
            #
            # ADD CODE HERE
            #

def game_loop(tank1, tank2, world):
    '''
    This method implements the game loop.
    The game loop basically consists of steps:
    (i) check if any events occurred. If that's the case, broadcast
    events to all event listeners
    (ii) Perform an update (tick) on all entities in the world.
    This includes the tanks, bases, missiles and the particle system.
    (iii) Render the new configuration of the world. Start with basic
    elements like the background and the bases. Afterwards, render the
    missiles, the tanks and at last the GUI elements. The order used
    for rendering is defined by the >priority< of each entity. The world
    list is sorted before rendering is performed in order to guarantee
    the order specified above
    (iv) Finally, we wait some time before performing the next loop
    '''
    
    clock = pygame.time.Clock()
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keys_pressed.append(event.key)
            elif event.type == pygame.KEYUP:
                keys_pressed.remove(event.key)
                
        # Broadcast events
        for l in input_listener:
            l.on_input(keys_pressed)

        screen.fill(pygame.Color(255, 255, 255)) # white
        # render background image
        #
        # ADD CODE HERE
        #
        
        # Sort world by priority
        world.sort()
        
        # entities:
        # update, remove "dead" ones, check for collision, render
        #
        # ADD CODE HERE
        #
        
        # Adjust framerate
        pygame.display.set_caption("FPS: %f" % (clock.get_fps(), ))
        pygame.display.flip()
        
        clock.tick(60)


if __name__ == '__main__':
    '''
    This is the program's starting point.
    We initialize the pygame module, create a screen and load
    resources (images etc.) in order to create the entities involved in
    the game.
    All entities are placed in a list, which we call world.
    At last, the game loop can be started using this list.
    '''
    
    # Initialize pygame and get a surface to draw on
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    
    
    # load the resources
    # initialize the basic entities (base, tank)
    #
    # ADD CODE HERE
    #
    
    # Add tanks to input listeners
    #
    # ADD CODE HERE
    #
    
    # Add both tanks to the world and start
    # the game loop
    #
    # ADD CODE HERE
    #