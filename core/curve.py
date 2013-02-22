import pygame, sys
from pygame import font
from math import sin, cos, pi
from random import Random

pygame.init()
size = width, height = 500, 500
black = 0, 0, 0
screen = pygame.display.set_mode(size)
rnd = Random()


class Player:

	TURN_SPEED = pi/50
	BREAK = 100
	BREAK_TIME = 13
	VELOCITY = 1.5
	INIT_TIME  = 100
	LINE_WIDTH = 6
	RADIUS = 4
	
	def __init__(self, x, y, name, color):
		self.name = name
		self.points = 0
		self.color = color
		self.location = [float(x), float(y)]
		self.last_location = [float(x), float(y)]
		self.velocity = Player.VELOCITY
		self.angle = 0.
		self.crossed_borders = False
		self.break_counter = Player.BREAK
		self.init_time = 0
	
	def turn(self, direction):
		self.angle = (self.angle - direction * Player.TURN_SPEED) % (pi*2)
	
	def move(self, velocity):
		return [self.x() + velocity * -sin(self.angle),\
				self.y() + velocity * -cos(self.angle)]
	
	def tick(self):
		self.last_location = self.location[:]
		self.location = self.move(self.velocity)
		
		# if self.init_time < Player.INIT_TIME:
			# self.crossed_borders = True
			# self.init_time += 1
		
		self.crossed_borders = False
		if self.location[0] < 0 or self.location[0] > width:
			self.location[0] %= width
			self.crossed_borders = True
		if self.location[1] < 0 or self.y() > height:
			self.location[1] %= height
			self.crossed_borders = True
		
		self.break_counter -= 1
		if self.break_counter < -Player.BREAK_TIME:
			self.break_counter = Player.BREAK
		if self.break_counter <= 0:
			self.crossed_borders = True
		
	def render(self, map):
		if not self.crossed_borders:
			print 'paint'
			pygame.draw.circle(map, self.color, (int(self.x()), int(self.y())), Player.RADIUS)
			pygame.draw.line(map, self.color, self.last_location, self.location, Player.LINE_WIDTH)
	
	def has_collided(self, map):
		x,y = self.move(Player.RADIUS+2)
		pixel = map.get_at((int(x%width), int(y%height)))
		return pixel[0:3] != (0, 0, 0)
	
	def x(self):
		return self.location[0]
	
	def y(self):
		return self.location[1]

		
p1 = Player(width/3, height/3, "Heinze", (255, 0, 0))
p2 = Player(width*2/3, height*2/3, "Steffen", (0, 0, 255))
p3 = Player(width/2, height/2, "Miggi", (0, 255, 0))
p4 = Player(width/2, height/2, "Max", (255, 255, 0))

keybinding = { 	pygame.K_q : [p1, -1], pygame.K_a : [p1, 1], \
				pygame.K_c : [p2, -1], pygame.K_v : [p2, 1],
				pygame.K_l : [p3, -1], pygame.K_o : [p3, 1],
				pygame.K_n : [p4, -1], pygame.K_m : [p4, 1]
			 }

all_players = [p1, p2, p3]
game_map = pygame.Surface(size)

if not font.get_init(): font.init()
cur_font = font.Font(font.get_default_font(), 12)

def init():
	players = all_players[:]
	for pl in players:
		x = int(rnd.random() * width)
		y = int(rnd.random() * height)
		pl.location = [x, y]
	game_map.fill ((0,0,0))
	return players, game_map

def get_pointlist(text):
	global cur_font
	return cur_font.render(text, True, (255, 255, 255))
	
def start_game():
	pressed = []
	players, game_map = init()
	while len(players) > 1:
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
		for pl in players:
			pl.tick()
			pl.render(game_map)
			if (pl.has_collided(game_map)):
				rm.append(pl)
		pt = len(rm)
		for pl in rm:
			players.remove(pl)
			print "%s is out!" % (pl.name, )
		for pl in players:
			pl.points += pt
		
		screen.blit(game_map, (0, 0, width, height))
		for pl in players: pygame.draw.circle(screen, pl.color, (int(pl.x()), int(pl.y())), Player.RADIUS)
		
		ranking = [(pl.points, pl.name) for pl in all_players]
		ranking.sort(reverse=True)
		pos = 10
		for line in ["%s:  %d points" % (p[1], p[0]) for p in ranking]:
			text = get_pointlist(line)
			screen.blit(text, (10, pos, text.get_width(), text.get_height()))
			pos += 15
				
		pygame.display.flip()
		pygame.time.wait(10)
	print "Game finished."



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				start_game()

