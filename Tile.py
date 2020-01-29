from Riddle import Riddle
from Spritesheet import Sprite


class Tile(object):
    TYPE_FLOOR = ' '
    TYPE_VOID = '#'
    TYPE_DOOR = '|'
    TYPE_START = 'S'
    TYPE_END = 'E'

    DIRECTION_UP = 0
    DIRECTION_RIGHT = 90
    DIRECTION_DOWN = 180
    DIRECTION_LEFT = 270

    def __init__(self, x, y, spritesheet, sprite_group, tile_scale):
        self.wall_sprite = Sprite(spritesheet, (64, 48, 16, 16), scale=tile_scale)
        self.floor_sprites = {
            0: Sprite(spritesheet, (32, 0, 16, 16), scale=tile_scale),
            1: Sprite(spritesheet, (0, 16, 16, 16), scale=tile_scale),
            2: {
                0: Sprite(spritesheet, (16, 0, 16, 16), scale=tile_scale, rotation=1),
                1: Sprite(spritesheet, (0, 0, 16, 16), scale=tile_scale, rotation=1)
            },
            3: Sprite(spritesheet, (48, 0, 16, 16), scale=tile_scale, rotation=2),
            4: Sprite(spritesheet, (64, 0, 16, 16), scale=tile_scale)
        }
        self.x = x
        self.y = y
        self.sprite_group = sprite_group
        self.tile_type = self.TYPE_VOID
        self.sprite = None
        self.step_neighbours = {}
        self.direct_neighbours = {}
        self.riddle = None

    def possible_stop_neighbours(self):
        possible = []
        for neighbour in self.step_neighbours.values():
            if neighbour[1].tile_type is self.TYPE_VOID:
                possible.append(neighbour)
        return possible

    def set_sprite(self):
        # Set correct sprites for floor tiles
        if self.tile_type in (self.TYPE_FLOOR, self.TYPE_START, self.TYPE_END):
            floor_neighbours_keys = []
            for key, neighbour in self.direct_neighbours.items():
                if neighbour.tile_type in (self.TYPE_FLOOR, self.TYPE_START, self.TYPE_END):
                    floor_neighbours_keys.append(key)

            floor_amount = len(floor_neighbours_keys)
            floor_direction = min(floor_neighbours_keys)

            if floor_amount is 2:
                if sum(floor_neighbours_keys) % 180 is 0:
                    # Straight line floor
                    self.sprite = self.floor_sprites[2][0]
                else:
                    # Corner floor
                    self.sprite = self.floor_sprites[2][1]
                    if min(floor_neighbours_keys) == 0 and max(floor_neighbours_keys) == 270:
                        floor_direction -= 90
            else:
                if floor_amount is 3:
                    for direction in (self.DIRECTION_UP, self.DIRECTION_RIGHT, self.DIRECTION_DOWN, self.DIRECTION_LEFT):
                        if direction not in floor_neighbours_keys:
                            floor_direction = direction
                self.sprite = self.floor_sprites[floor_amount]

            self.sprite.rotate(floor_direction)
            self.sprite.set_pos((self.x * self.sprite.size[0], self.y * self.sprite.size[1]))
            self.sprite.add(self.sprite_group)

        # Set correct sprites for void tiles (to be implemented)
        elif self.tile_type is self.TYPE_VOID:
            return

    def update_type(self, tile_type):
        self.tile_type = tile_type
        # if tile_type in (self.TYPE_FLOOR, self.TYPE_START, self.TYPE_END):
        #     self.sprite.remove(self.sprite_group)
