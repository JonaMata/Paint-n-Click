import sys
import pygame
from levels import LevelManager


class Game:
	def __init__(self):
		pygame.init()
		self.size = (500, 500)
		self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

		# initialize time variables
		self.time = pygame.time.get_ticks()
		self.dt = 0

		self.level_manager = LevelManager(self.size)

	def game_loop(self):
		# set delta time
		current_time = pygame.time.get_ticks()
		self.dt = current_time - self.time
		self.time = current_time

		self.handle_events()
		self.update(self.dt)
		self.render()

	def update(self, dt):
		self.level_manager.level.update(dt)

	def render(self):
		self.screen.fill((255, 255, 255))
		self.level_manager.level.render(self.screen)
		pygame.display.flip()

	def handle_events(self):
		if pygame.event.get(pygame.QUIT):
			sys.exit()
		self.level_manager.level.handle_events(pygame.event.get())


if __name__ == "__main__":
	g = Game()
	while True:
		g.game_loop()
