
import sys, pygame, os
from entities import *

pygame.init()

size = width, height = 800, 600
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = Entity(100, 100, pygame.image.load("tank1.gif"))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball.accelerate(-1, 0)
            elif event.key == pygame.K_RIGHT:
                ball.accelerate(1, 0)
            elif event.key == pygame.K_UP:
                ball.accelerate(0, -1)
            elif event.key == pygame.K_DOWN:
                ball.accelerate(0, 1)
    ball.move()
    screen.fill(black)
    ball.render(screen)
    pygame.display.flip()
    pygame.time.wait(10)
