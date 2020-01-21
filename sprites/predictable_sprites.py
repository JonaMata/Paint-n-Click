import pygame


class Key(pygame.sprite.Sprite):
	def __init__(self, size, color):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("sprites/png/key.png"), (size, size))
		self.radius = int(size / 2)
		self.rect = self.image.get_rect(center=(self.radius, self.radius))
		self.color = color
