# This class handles sprite sheets
# Taken from https://www.pygame.org/wiki/Spritesheet
# Note: When calling images_at the rect is the format:
# (x, y, x_offset, y_offset)

import pygame


class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Loads multiple images, supply a list of coordinates
    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    # Loads a strip of images and returns them as a list
    def load_strip(self, rect, image_count, colorkey=None):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


# Note: load_pos should be in the form of:
# (x, y, x_offset, y_offset)
class Sprite(pygame.sprite.Sprite):
    def __init__(self, spritesheet, pos, load_pos, rotation=0, scale=4, colorkey=(0, 255, 0)):
        super().__init__()
        self.image = spritesheet.image_at(load_pos, colorkey)
        self.image = pygame.transform.rotate(self.image, rotation*90)
        self.image = pygame.transform.scale(self.image, (load_pos[2]*scale, load_pos[3]*scale))
        self.rect = self.image.get_rect(center=(load_pos[2]*scale//2, load_pos[3]*scale//2))
        self.rect.x = pos[0]
        self.rect.y = pos[1]
