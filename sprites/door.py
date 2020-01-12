import pygame
import pygame.gfxdraw


class Door(pygame.sprite.Sprite):
	def __init__(self, pos, size):
		super().__init__()
		self.images = (
			pygame.transform.scale(pygame.image.load("sprites/png/door.png"), (size, size)),
			pygame.transform.scale(pygame.image.load("sprites/png/door_open.png"), (size, size))
		)
		self.image = self.images[0]
		self.rect = self.image.get_rect(center=(size / 2, size / 2))
		self.rect.x = pos[0]-size/2
		self.rect.y = pos[1]-size/2

	def open(self):
		self.image = self.images[1]
