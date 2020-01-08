import sys, pygame


class Game:
	def __init__(self):
		pygame.init()
		self.white = 255, 255, 255
		# infoObject = pygame.display.Info()
		# size = (infoObject.current_w, infoObject.current_h)
		self.size = (500, 500)
		self.time = pygame.time.get_ticks()
		self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

		self.door = pygame.transform.scale(pygame.image.load("sprites/door.png"), (100, 100))
		self.door_rect = self.door.get_rect()
		self.door_pos = (self.size[0] / 2 - self.door_rect.center[0], self.size[1] / 2 - self.door_rect.center[1])


	def game_loop(self):
		current_time = pygame.time.get_ticks()
		self.delta_time = current_time - self.time
		self.time = current_time
		self.handle_events()
		self.update_game(self.delta_time)
		self.draw_components()

	def update_game(self, dt):
		# update loop
		pass

	def draw_components(self):
		self.screen.fill(self.white)

		self.screen.blit(self.door, self.door_pos)

		pygame.display.flip()

	def wait_for(self, wait_time): # waitTime in milliseconds
		screen_copy = self.screen.copy()
		wait_count = 0
		while wait_count < wait_time:
			wait_count += self.delta_time
			pygame.event.pump() # Tells pygame to handle it's event, instead of pygame.event.get()
			self.screen.blit(screen_copy, (0, 0))
			pygame.display.flip()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.handle_mouse_pressed()

	def handle_mouse_pressed(self):
		self.door = pygame.transform.scale(pygame.image.load("sprites/door_open.png"), (100, 100))
		self.screen.fill(self.white)
		self.screen.blit(self.door, self.door_pos)
		self.wait_for(2000)
		self.door = pygame.transform.scale(pygame.image.load("sprites/door.png"), (100, 100))


if __name__ == "__main__":
	g = Game()
	while True:
		g.game_loop()