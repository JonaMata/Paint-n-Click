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
    def __init__(self, spritesheet=None, load_pos=(0, 0, 16, 16), pos=(0, 0), rotation=0, scale=4, flip=None, colorkey=(0, 255, 0), image=None):
        super().__init__()
        if image:
            self.image = image
        elif spritesheet:
            self.image = spritesheet.image_at(load_pos, colorkey)
        self.size = (int(load_pos[2] * scale), int(load_pos[3] * scale))

        if rotation > 0:
            self.image = pygame.transform.rotate(self.image, rotation*90)
        if scale > 1:
            self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        if flip:
            self.image = pygame.transform.flip(self.image, flip[0], flip[1])

        self.rect = self.image.get_rect(center=(self.size[0]//2, self.size[1]//2))
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]