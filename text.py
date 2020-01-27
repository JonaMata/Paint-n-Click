import pygame


class Text:
	def __init__(self, text, pos, size='medium', center=True, color=(0, 0, 0)):
		self.fonts = {
			"small": pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 16),
			"medium": pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 24),
			"large": pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 48),
		}
		self.size = size
		self.color = color
		self.surface = self.fonts[size].render(text, True, color)
		self.rect = self.surface.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]

		if center:
			self.rect.x -= self.rect.width / 2
			self.rect.y -= self.rect.height / 2

	def render(self, screen):
		screen.blit(self.surface, self.rect)

	def set_text(self, text):
		self.surface = self.fonts[self.size].render(text, True, self.color)
