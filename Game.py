import sys
import pygame
from Screens import ScreenManager


class Game(object):
	def __init__(self):
		pygame.init()
		self.size = (640, 640)
		self.screen = pygame.display.set_mode(self.size)

		self.time = pygame.time.get_ticks()
		self.dt = 0

		self.screen_manager = ScreenManager(self.size)

	def game_loop(self):
		current_time = pygame.time.get_ticks()
		self.dt = current_time - self.time
		self.time = current_time

		self.handle_events()
		self.update(self.dt)
		self.render()

	def update(self, dt):
		self.screen_manager.current_screen.update(dt)

	def render(self):
		self.screen_manager.current_screen.render(self.screen)
		pygame.display.flip()

	def handle_events(self):
		if pygame.event.get(pygame.QUIT):
			self.screen_manager.drawing_camera.release()
			sys.exit()
		self.screen_manager.current_screen.handle_events(pygame.event.get())


if __name__ == "__main__":
	g = Game()
	while True:
		g.game_loop()

