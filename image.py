import pygame


class Image(pygame.sprite.Sprite):
	def __init__(self, image_path, pos, size):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load(image_path), (size, size))
		self.radius = int(size / 2)
		self.rect = self.image.get_rect(center=(self.radius, self.radius))
		self.rect.x = pos[0] - size / 2
		self.rect.y = pos[1] - size / 2
