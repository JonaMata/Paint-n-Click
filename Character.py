from Spritesheet import *


class Character(pygame.sprite.Sprite):
    def __init__(self, pos, tile_scale, animation_speed=1, speed=2, colorkey=(0, 255, 0)):
        super().__init__()
        # Character from https://0x72.itch.io/dungeontileset-ii
        spritesheet = SpriteSheet("assets/png/character.png")
        sprite_size = (16, 22)
        self.idle = [
            spritesheet.image_at((0, 5, sprite_size[0], sprite_size[1]), colorkey),
            spritesheet.image_at((16, 5, sprite_size[0], sprite_size[1]), colorkey),
            spritesheet.image_at((32, 5, sprite_size[0], sprite_size[1]), colorkey),
            spritesheet.image_at((48, 5, sprite_size[0], sprite_size[1]), colorkey),
        ]
        self.running = [
            spritesheet.image_at((64, 5, sprite_size[0], sprite_size[1]), colorkey),
            spritesheet.image_at((80, 5, sprite_size[0], sprite_size[1]), colorkey),
            spritesheet.image_at((96, 5, sprite_size[0], sprite_size[1]), colorkey),
            spritesheet.image_at((112, 5, sprite_size[0], sprite_size[1]), colorkey),
        ]

        self.tile_scale = tile_scale
        self.speed = speed
        self.direction = (0, 0)
        self.animation_speed = animation_speed
        self.size = (int(sprite_size[0] * self.tile_scale), int(sprite_size[1] * self.tile_scale))
        self.is_running = False
        self.flipped = False
        self.frame = 0
        self.image = self.idle[self.frame]
        self.rect = self.image.get_rect(center=(self.size[0] // 2, self.size[1] // 2))
        self.hitbox = pygame.rect.Rect((0, 0), (1 * tile_scale, 1 * tile_scale), center=(self.size[0] // 2, self.size[1] // 2))
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def render(self, screen):
        if self.is_running:
            current_animation = self.running
        else:
            current_animation = self.idle

        if self.frame + 1 > (len(self.running)) * self.animation_speed:
            self.frame = 0

        if self.flipped:
            self.image = pygame.transform.flip(current_animation[self.frame // self.animation_speed], 1, 0)
        else:
            self.image = current_animation[self.frame // self.animation_speed]

        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        screen.blit(self.image, self.rect)
        self.frame += 1

    def update(self):
        if self.is_running:
            self.rect.x += self.direction[0] * self.speed
            self.hitbox.x = self.rect.x+self.size[0]//2
            self.rect.y += self.direction[1] * self.speed
            self.hitbox.y = self.rect.y+self.size[1]//2+5

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = (-1, 0)
            self.flipped = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = (1, 0)
            self.flipped = False
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = (0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = (0, 1)
        else:
            self.direction = (0, 0)

        if self.direction[0] is not 0 or self.direction[1] is not 0:
            self.is_running = True
        else:
            self.is_running = False

    # Handle a collision so the character can not walk into non-floor tiles
    def collide(self, other):
        if self.direction[0] > 0:
            self.rect.right = other.rect.left
        elif self.direction[0] < 0:
            self.rect.left = other.rect.right
        elif self.direction[1] > 0:
            self.rect.bottom = other.rect.top
        elif self.direction[1] < 0:
            self.rect.top = other.rect.bottom
