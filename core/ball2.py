import sys, pygame

class Ball:
    
    # Konstruktor
    def __init__(self):
        self.image = pygame.image.load('ball.gif')
        self.img_rect = self.image.get_rect()
        self.speed = [2, 2]
        self.pos = [100, 100]
        
    def render(self, screen):
        '''
        Diese Methode zeigt den Ball auf dem Spielfeld an
        '''
        screen.blit(self.image, self.img_rect)
    
    def move(self):
        self.pos = [self.pos[0] + self.speed[0],
                    self.pos[1] + self.speed[1]]
        if self.pos[0] < 0 or self.pos[0]+self.img_rect.width > width:
            self.speed[0] = -self.speed[0]
        if self.pos[1] < 0 or self.pos[1]+self.img_rect.height > height:
            self.speed[1] = -self.speed[1]
        self.img_rect.left, self.img_rect.right = self.pos

pygame.init()

size = width, height = 320, 240
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = Ball()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    ball.move()
    ball.render(screen)
    pygame.display.flip()
    pygame.time.wait(10)