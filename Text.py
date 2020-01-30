import pygame


class Text:
	def __init__(self, text, pos, size='medium', center=True, color=(0, 0, 0), width=200):
		self.fonts = {
			"small": pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 16),
			"medium": pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 24),
			"large": pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 48),
		}
		self.font = self.fonts[size]
		self.width = width
		self.color = color
		self.text = text
		self.surface = self.font.render(text, True, color)
		self.rect = self.surface.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]

		if center:
			self.rect.x -= self.rect.width / 2
			self.rect.y -= self.rect.height / 2

	def render(self, screen):
		screen.blit(self.surface, self.rect)

	def set_text(self, text):
		self.surface = self.font.render(text, True, self.color)
