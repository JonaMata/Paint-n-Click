import pygame


class DoorIntro(pygame.sprite.Sprite):
	def __init__(self, pos, size):
		super().__init__()
		self.images = (
			pygame.transform.scale(pygame.image.load("assets/png/door.png"), (size, size)),
			pygame.transform.scale(pygame.image.load("assets/png/door_open.png"), (size, size))
		)
		self.image = self.images[0]
		self.rect = self.image.get_rect(center=(size / 2, size / 2))
		self.rect.x = pos[0]-size/2
		self.rect.y = pos[1]-size/2
		self.is_open = False

	def open(self):
		self.image = self.images[1]
		self.is_open = True
