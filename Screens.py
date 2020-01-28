from Spritesheet import *
from Door import Door
from Character import Character
from Maze import Maze
from DrawingCamera import DrawingCamera
from Text import Text
import pygame


class Screen:
	def __init__(self, size, manager, drawing_camera):
		self.colors = {
			"white": (255, 255, 255),
			"black": (0, 0, 0),
			"background": (255, 255, 255)
		}

		# Tilemap heavily inspired by "Dungeon Tilemap" by Michele Bucelli https://opengameart.org/users/buch?page=2
		self.spritesheet = SpriteSheet("assets/png/tilemap.png")
		self.screen_name = "Unnamed Screen"
		self.screen_center = (size[0] // 2, size[1] // 2)
		self.manager = manager
		self.next_screen = self.manager.screens[0]
		self.sprite_list = pygame.sprite.Group()
		self.text = {}
		self.timer = 0
		self.drawing_camera = drawing_camera

	def render(self, screen):
		screen.fill(self.colors["background"])
		self.sprite_list.draw(screen)
		for text in self.text:
			text.render(screen)

	def update(self, dt):
		self.drawing_camera.update()
		self.sprite_list.update(dt)

	def handle_events(self, events):
		pass


class ScreenManager:
	def __init__(self, size):
		self.size = size
		self.drawing_camera = DrawingCamera()
		self.screens = Screen.__subclasses__()
		self.initial_screen = self.screens[1]
		self.current_screen = self.initial_screen(self.size, self, self.drawing_camera)

	def next(self):
		self.current_screen = self.current_screen.next_screen(self.size, self, self.drawing_camera)
		print("going to {}".format(self.current_screen.screen_name))


class IntroScreen(Screen):
	def __init__(self, size, manager, drawing_camera):
		super().__init__(size, manager, drawing_camera)
		self.next_screen = self.manager.screens[1]
		self.screen_name = "Intro"
		self.text = {
			Text("Paint 'n Click", (self.screen_center[0], self.screen_center[1] - 100), 'large'),
			Text("Draw the right solution and", (self.screen_center[0], self.screen_center[1] + 80), 'medium'),
			Text("capture it with you webcam", (self.screen_center[0], self.screen_center[1] + 110), 'medium'),
			Text("click to continue!", (self.screen_center[0], self.screen_center[1] + 150), 'small')
		}
		self.door = Door(self.screen_center, 100)
		self.sprite_list.add(self.door)

	def update(self, dt):
		super().update(dt)
		if self.door.is_open:
			self.timer += dt
			if self.timer >= 1500:
				self.manager.next()

	def handle_events(self, events):
		for event in events:
			if event.type is pygame.MOUSEBUTTONDOWN:
				self.door.open()


class MazeScreen(Screen):
	def __init__(self, size, manager, drawing_camera):
		super().__init__(size, manager, drawing_camera)
		self.character = Character((0, 24), 3)
		self.maze = Maze(size[0]//10, size[1]//10)
		self.colors["background"] = (33, 30, 39)
		self.next_screen = self.manager.screens[2]
		self.screen_name = "Maze"

	def render(self, screen):
		super().render(screen)
		self.character.render(screen)

	def handle_events(self, events):
		for event in events:
			if event.type is pygame.MOUSEBUTTONDOWN:
				self.manager.next()


class OutroScreen(Screen):
	def __init__(self, size, manager, drawing_camera):
		super().__init__(size, manager, drawing_camera)
		self.next_screen = self.manager.screens[0]
		self.screen_name = "Outro"

	def handle_events(self, events):
		for event in events:
			if event.type is pygame.MOUSEBUTTONDOWN:
				self.manager.next()
