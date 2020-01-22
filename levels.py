from assets.sprites.door import Door
from assets.sprites.solutions import Solution
from drawing_camera import DrawingCamera
from text import Text
import pygame


class Level:
	def __init__(self, size, manager, drawing_camera, end_counter):
		self.colors = {
			"white": (255, 255, 255),
			"black": (0, 0, 0),
			"green": (0, 255, 0)
		}

		self.screen_center = (size[0]//2, size[1]//2)
		self.door = Door(self.screen_center, 100)
		self.manager = manager
		self.is_completed = False
		self.end_counter = end_counter

		self.level_index_text = Text("Level {}".format(self.manager.level_index), (5, 0), 'medium', False)

		self.question = None
		self.solution = None
		self.solution_sprite = None

		self.sprite_list = pygame.sprite.Group()

		self.drawing_camera = drawing_camera

	def render(self, screen):
		screen.fill(self.colors["white"])
		self.level_index_text.render(screen)
		if self.question is not None:
			self.question.render(screen)
		self.sprite_list.draw(screen)

	def update(self, dt):
		if self.is_completed and self.end_counter > 0:
			self.end_counter -= dt
		elif self.end_counter <= 0:
			self.manager.next_level()
		else:
			self.drawing_camera.update()
			self.check_solution(self.drawing_camera.get_prediction())
			self.sprite_list.update(dt)

	def check_solution(self, prediction):
		if self.solution and prediction is not None:
			if self.solution in prediction and self.is_completed is False:
				self.complete()

	def handle_events(self, events):
		pass

	def complete(self):
		self.is_completed = True
		if self.solution_sprite is not None:
			self.sprite_list.add(self.solution_sprite)


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
		self.level = self.levels[level](self.size, self, self.drawing_camera, 1500)

	def next_level(self):
		self.level_index += 1
		next_level = self.level_index
		self.go_to(next_level)


class LevelZero(Level):
	def __init__(self, size, manager, drawing_camera, end_counter):
		super(LevelZero, self).__init__(size, manager, drawing_camera, end_counter)
		self.text = {
			Text("Paint 'n Click", (self.screen_center[0], self.screen_center[1]-100), 'large'),
			Text("Draw the right solution and", (self.screen_center[0], self.screen_center[1]+80), 'medium'),
			Text("capture it with you webcam", (self.screen_center[0], self.screen_center[1] + 110), 'medium'),
			Text("click to continue!", (self.screen_center[0], self.screen_center[1]+150), 'small')
		}
		self.sprite_list.add((
			self.door
		))

	def render(self, screen):
		super().render(screen)
		for text in self.text:
			text.render(screen)

	def handle_events(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.complete()

	def complete(self):
		super().complete()
		self.door.open()


class LevelOne(Level):
	def __init__(self, size, manager, drawing_camera, end_counter):
		super(LevelOne, self).__init__(size, manager, drawing_camera, end_counter)
		self.question = Text("Door = Locked", (self.screen_center[0], 50), 'medium')
		self.solution = "key"
		self.solution_sprite = Solution("assets/png/key.png", (self.screen_center[0], 130), 100)
		self.sprite_list.add((
			self.door
		))

	def handle_events(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.check_solution("key")

	def complete(self):
		super().complete()
		self.door.open()


class LevelTwo(Level):
	def __init__(self, size, manager, drawing_camera, end_counter):
		super(LevelTwo, self).__init__(size, manager, drawing_camera, end_counter)
		self.question = Text("Can you help me get home?", (self.screen_center[0], 50), 'medium')
		self.solution = "key"
		self.solution_sprite = Solution("assets/png/key.png", (self.screen_center[0], 130), 100)

	def handle_events(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.check_solution("car")
