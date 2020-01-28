from Spritesheet import *


class Character:
    def __init__(self, pos, animation_speed):
        # Character from https://0x72.itch.io/dungeontileset-ii
        spritesheet = SpriteSheet("assets/png/character.png")
        self.is_running = False
        self.frame = 0
        self.animation_speed = animation_speed
        self.flipped = True
        self.pos = pos
        self.idle = [
            Sprite(spritesheet, (0, 0, 16, 27)),
            Sprite(spritesheet, (16, 0, 16, 27)),
            Sprite(spritesheet, (32, 0, 16, 27)),
            Sprite(spritesheet, (48, 0, 16, 27)),
        ]
        self.running = [
            Sprite(spritesheet, (64, 0, 16, 27)),
            Sprite(spritesheet, (80, 0, 16, 27)),
            Sprite(spritesheet, (96, 0, 16, 27)),
            Sprite(spritesheet, (112, 0, 16, 27)),
        ]

    def render(self, screen):
        if self.is_running:
            current_animation = self.running
        else:
            current_animation = self.idle

        if self.frame + 1 > (len(self.running)) * self.animation_speed:
            self.frame = 0

        if self.flipped:
            current_frame = pygame.transform.flip(current_animation[self.frame // self.animation_speed].image, 1, 0)
        else:
            current_frame = self.running[self.frame // self.animation_speed].image
        self.frame += 1
        screen.blit(current_frame, self.pos)



