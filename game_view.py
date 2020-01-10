import sys
import pygame
from sprites.ball import Ball
from sprites.door import Door


class Game:
	def __init__(self):
		pygame.init()
		self.size = (500, 500)
		self.center = (self.size[0]/2, self.size[1]/2)
		self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

		# initialize time variables
		self.time = pygame.time.get_ticks()
		self.delta_time = 0

		# set colors
		self.colors = {
			"white": (255, 255, 255),
			"black": (0, 0, 0)
		}

		# Assign sprites
		self.door = Door(self.center, 100)
		self.ball = Ball(30, self.colors["black"])

		self.sprite_list = pygame.sprite.Group()
		self.sprite_list.add((
			self.ball,
			self.door
		))

	def game_loop(self):
		current_time = pygame.time.get_ticks()
		self.delta_time = current_time - self.time
		self.time = current_time

		self.handle_events()
		self.update_game(self.delta_time)
		self.draw_components()

	def update_game(self, dt):
		self.sprite_list.update(dt)

	def draw_components(self):
		self.screen.fill(self.colors["white"])

		self.sprite_list.draw(self.screen)

		pygame.display.flip()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.handle_mouse_pressed()
			if event.type == pygame.MOUSEMOTION:
				self.handle_mouse_motion()

	def handle_mouse_pressed(self):
		self.door.handle_mouse_pressed()

	def handle_mouse_motion(self):
		self.ball.handle_mouse_motion(pygame.mouse.get_pos())


if __name__ == "__main__":
	g = Game()
	while True:
		g.game_loop()
