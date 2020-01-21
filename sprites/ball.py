import pygame
import pygame.gfxdraw


class Ball(pygame.sprite.Sprite):
	def __init__(self, size, color):
		super().__init__()
		self.image = pygame.Surface((size, size), pygame.SRCALPHA)
		self.radius = int(size / 2)
		self.rect = self.image.get_rect(center=(self.radius, self.radius))
		self.color = color
		pygame.gfxdraw.filled_circle(self.image, self.rect.center[0], self.rect.center[1], self.radius, color)
