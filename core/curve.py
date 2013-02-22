import pygame, sys
from pygame import font
from math import sin, cos, pi
from vector import Vector2D

pygame.init()
size = width, height = 500, 500
black = (0, 0, 0)
screen = pygame.display.set_mode(size)

p1 = Player(width/3, height/3, "Red", (255, 0, 0))
p2 = Player(width*2/3, height*2/3, "Blue", (0, 0, 255))

keybinding = { 	pygame.K_y : [p1, -1], pygame.K_x : [p1, 1], \
				pygame.K_n : [p2, -1], pygame.K_m : [p2, 1]
			 }

all_players = [p1, p2]
game_map = pygame.Surface(size)

class Player:

	TURN_SPEED = pi/50
	BREAK = 100
	BREAK_TIME = 13
	VELOCITY = 1.5
	LINE_WIDTH = 6
	RADIUS = 4
	
	def __init__(self, x, y, name, color):
		self.name = name
		self.points = 0
		self.color = color
		self.location = Vector2D(x, y)
		self.velocity = Player.VELOCITY
		self.angle = 0.
		self.draw_line = True
		self.break_counter = Player.BREAK
	
	def turn(self, direction):
		self.angle = (self.angle - direction * Player.TURN_SPEED) % (pi*2)
	
	def move(self, velocity):
		return self.location + Vector2D(sin(self.angle), cos(self.angle)) * -velocity
	
	def tick(self):
		self.location = self.move(self.velocity)
		self.draw_line = not self.check_borders() or self.check_break()
	
	def check_break(self):
		self.break_counter -= 1
		if self.break_counter < -Player.BREAK_TIME:
			self.break_counter = Player.BREAK
		if self.break_counter <= 0:
			return True
		return False
	
	def check_borders(self):
		if self.x() < 0 or self.x() > width:
			self.location[0] %= width
			return True
		if self.y() < 0 or self.y() > height:
			self.location[1] %= height
			return True
		return False
		
	def render(self, map):
		if not self.crossed_borders:
			pygame.draw.circle(map, self.color, (int(self.x()), int(self.y())), Player.RADIUS)
	
	def has_collided(self, map):
		x,y = self.move(Player.RADIUS+2)
		pixel = map.get_at((int(x%width), int(y%height)))
		return pixel[0:3] != (0, 0, 0)
	
	def x(self):
		return self.location[0]
	
	def y(self):
		return self.location[1]
	
	def alive(self):
		pass

def init():
	players = all_players[:]
	game_map.fill (black)
	return players, game_map
	
def start_game():
	pressed = []
	players, game_map = init()
	while len(players) > 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if keybinding.has_key(event.key):
					pressed.append(event.key)
			if event.type == pygame.KEYUP:
				if keybinding.has_key(event.key) and event.key in pressed:
					pressed.remove(event.key)
			
		for key in pressed:
			player, action = keybinding[key]
			player.turn(action)
		
		rm = []
		for i in range(len(players)):
			pl = players[i]
			pl.tick()
			pl.render(game_map)
			if pl.has_collided(game_map):
				players.pop(i)
				
		screen.blit(game_map, (0, 0, width, height))
		
		for pl in players: pygame.draw.circle(screen, pl.color, (int(pl.x()), int(pl.y())), Player.RADIUS)
				
		pygame.display.flip()
		pygame.time.wait(10)
		
	ranking = [(pl.points, pl.name) for pl in all_players]
	ranking.sort(reverse=True)
	for line in ["%s:  %d points" % (p[1], p[0]) for p in ranking]:
		text = get_pointlist(line)
		print text


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				start_game()

