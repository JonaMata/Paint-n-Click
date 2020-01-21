import pygame
from sprites.ball import Ball
from sprites.door import Door
from drawing_camera import DrawingCamera


class Level:
	def __init__(self, size, manager, drawing_camera):
		self.colors = {
			"white": (255, 255, 255),
			"black": (0, 0, 0),
			"green": (0, 255, 0)
		}

		self.door = Door((size[0]/2, size[1]/2), 100)
		self.manager = manager
		self.finished = False
		self.solution = " "

		self.sprite_list = pygame.sprite.Group()
		self.sprite_list.add((
			self.door
		))

		self.drawing_camera = drawing_camera

	def render(self, screen):
		self.sprite_list.draw(screen)

	def update(self, dt):
		self.drawing_camera.update()
		self.check_solution(self.drawing_camera.get_prediction())
		self.sprite_list.update(dt)

	def check_solution(self, prediction):
		if self.solution in prediction and self.finished is False:
			self.finished = True
			self.door.open()

	def handle_events(self, events):
		pass


class LevelManager:
	def __init__(self, size):
		self.size = size
		self.levels = Level.__subclasses__()
		self.level = None
		self.level_index = 0
		self.drawing_camera = DrawingCamera()
		self.go_to(self.level_index)

	def go_to(self, level):
		print("going to level {}".format(level))
		self.level = self.levels[level](self.size, self, self.drawing_camera)

	def next_level(self):
		next_level = self.level_index+1
		print("going to level {}".format(next_level))
		self.level = self.levels[next_level](self.size, self, self.drawing_camera)


class LevelZero(Level):
	def __init__(self, size, manager, drawing_camera):
		super(LevelZero, self).__init__(size, manager, drawing_camera)
		self.ball = Ball(30, self.colors["black"])
		self.sprite_list.add(self.ball)
		self.solution = "key"

	def handle_events(self, events):
		for event in events:
			if event.type == pygame.MOUSEMOTION:
				self.ball.rect.x = pygame.mouse.get_pos()[0] - self.ball.radius
				self.ball.rect.y = pygame.mouse.get_pos()[1] - self.ball.radius
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.check_solution(prediction="key")


class LevelOne(Level):
	def __init__(self, size, manager, drawing_camera):
		super(LevelOne, self).__init__(size, manager, drawing_camera)
		self.ball = Ball(30, self.colors["green"])
		self.sprite_list.add(self.ball)

	def handle_events(self, events):
		for event in events:
			if event.type == pygame.MOUSEMOTION:
				self.ball.rect.x = pygame.mouse.get_pos()[0] - self.ball.radius
				self.ball.rect.y = pygame.mouse.get_pos()[1] - self.ball.radius
