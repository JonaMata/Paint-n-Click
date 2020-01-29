from Spritesheet import Sprite
from Riddle import Riddle


class Door(Sprite):
    def __init__(self, spritesheet, load_pos=(0, 32, 16, 26), pos=(0, 0), rotation=0, scale=4, flip=None,
                 colorkey=(0, 255, 0)):
        super().__init__(spritesheet, load_pos, pos, rotation, scale, flip, colorkey)
        self.is_open = False
        self.riddle = Riddle()
        self.scale = scale
        self.collided = False

    def render_riddle(self, screen):
        if self.collided is True:
            self.riddle.render(screen)
        self.collided = False

    def open(self):
        self.is_open = True
        self.kill()

    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1] - self.scale*10

    def collide(self):
        self.collided = True



