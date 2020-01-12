import pygame
import pygame.gfxdraw


class Ball(pygame.sprite.Sprite):
	def __init__(self, size, color):
		super().__init__()
		self.image = pygame.Surface((size, size), pygame.SRCALPHA)
		self.rect = self.image.get_rect(center=(size / 2, size / 2))
		self.radius = int(size / 2)
		self.color = color
		pygame.gfxdraw.filled_circle(self.image, self.rect.center[0], self.rect.center[1], self.radius, color)
