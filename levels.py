import pygame
from sprites.ball import Ball
from sprites.door import Door


class Level:
	def __init__(self, size, manager):
		self.colors = {
			"white": (255, 255, 255),
			"black": (0, 0, 0),
			"green": (0, 255, 0)
		}

		self.door = Door((size[0]/2, size[1]/2), 100)
		self.manager = manager

		self.sprite_list = pygame.sprite.Group()
		self.sprite_list.add((
			self.door
		))

	def render(self, screen):
		self.sprite_list.draw(screen)

	def update(self, dt):
		self.sprite_list.update(dt)

	def handle_events(self, events):
		pass


class LevelManager:
	def __init__(self, size):
		self.size = size
		self.levels = Level.__subclasses__()
		self.level = None
		self.go_to(0)

	def go_to(self, level):
		print("going to level {}".format(level))
		self.level = self.levels[level](self.size, self)


class LevelZero(Level):
	def __init__(self, size, manager):
		super(LevelZero, self).__init__(size, manager)
		self.ball = Ball(30, self.colors["black"])
		self.sprite_list.add(self.ball)

	def handle_events(self, events):
		for event in events:
			if event.type == pygame.MOUSEMOTION:
				self.ball.rect.x = pygame.mouse.get_pos()[0] - self.ball.radius
				self.ball.rect.y = pygame.mouse.get_pos()[1] - self.ball.radius
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.manager.go_to(1)


class LevelOne(Level):
	def __init__(self, size, manager):
		super(LevelOne, self).__init__(size, manager)
		self.ball = Ball(30, self.colors["green"])
		self.sprite_list.add(self.ball)

	def handle_events(self, events):
		for event in events:
			if event.type == pygame.MOUSEMOTION:
				self.ball.rect.x = pygame.mouse.get_pos()[0] - self.ball.radius
				self.ball.rect.y = pygame.mouse.get_pos()[1] - self.ball.radius
