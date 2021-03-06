from Spritesheet import Sprite
from Door import Door


class Tile(object):
    TYPE_FLOOR = ' '
    TYPE_VOID = '#'
    TYPE_DOOR = '|'
    TYPE_START = 'S'
    TYPE_END = 'E'

    DIRECTION_UP = 0
    DIRECTION_RIGHT = 3
    DIRECTION_DOWN = 2
    DIRECTION_LEFT = 1

    def __init__(self, x, y, spritesheet, maze_sprite_group, void_sprite_group, door_sprite_group, tile_scale):
        self.pillar_sprite = Sprite(spritesheet, (32, 16, 16, 16), scale=tile_scale)
        self.door_sprite = Door(spritesheet, (0, 32, 16, 26), scale=tile_scale)
        self.void_sprite = Sprite(spritesheet, (48, 64, 16, 16), scale=tile_scale)
        self.floor_sprites = {
            0: Sprite(spritesheet, (32, 0, 16, 16), scale=tile_scale),
            1: Sprite(spritesheet, (0, 16, 16, 16), scale=tile_scale),
            2: {
                0: Sprite(spritesheet, (16, 0, 16, 16), scale=tile_scale, rotation=1),
                1: Sprite(spritesheet, (0, 0, 16, 16), scale=tile_scale, rotation=2)
            },
            3: Sprite(spritesheet, (48, 0, 16, 16), scale=tile_scale, rotation=2),
            4: Sprite(spritesheet, (64, 0, 16, 16), scale=tile_scale)
        }
        self.x = x
        self.y = y
        self.maze_sprite_group = maze_sprite_group
        self.void_sprite_group = void_sprite_group
        self.door_sprite_group = door_sprite_group
        self.tile_type = self.TYPE_VOID
        self.tile_size = tile_scale*16
        self.sprite = None
        self.step_neighbours = {}
        self.direct_neighbours = {}

        # Pathfinding variables
        self.h_score = 0
        self.g_score = 0
        self.is_seen = False
        self.is_visited = False
        self.parent = None

    def possible_stop_neighbours(self):
        possible = []
        for neighbour in self.step_neighbours.values():
            if neighbour[1].tile_type is self.TYPE_VOID:
                possible.append(neighbour)
        return possible

    def set_sprite(self):
        # Set correct sprites for floor tiles
        if self.tile_type is self.TYPE_FLOOR:
            floor_neighbours_keys = self.floor_neighbours().keys()
            floor_amount = len(floor_neighbours_keys)
            if floor_amount is 0:
                self.sprite = self.floor_sprites[0]
            else:
                floor_direction = min(floor_neighbours_keys)

                if floor_amount is 2:
                    if sum(floor_neighbours_keys) % 2 is 0:
                        # Straight line floor
                        self.sprite = self.floor_sprites[2][0]
                    else:
                        # Corner floor
                        self.sprite = self.floor_sprites[2][1]
                        if min(floor_neighbours_keys) == 0 and max(floor_neighbours_keys) == 3:
                            floor_direction -= 1
                else:
                    if floor_amount is 3:
                        for direction in (self.DIRECTION_UP, self.DIRECTION_RIGHT, self.DIRECTION_DOWN, self.DIRECTION_LEFT):
                            if direction not in floor_neighbours_keys:
                                floor_direction = direction
                    self.sprite = self.floor_sprites[floor_amount]

                self.sprite.rotate(floor_direction)

        # Set correct sprites for void tiles (to be implemented)
        elif self.tile_type is self.TYPE_VOID:
            if self.DIRECTION_UP in self.direct_neighbours and self.direct_neighbours[self.DIRECTION_UP].tile_type in (self.TYPE_FLOOR, self.TYPE_DOOR):
                self.sprite = self.pillar_sprite
            else:
                self.sprite = self.void_sprite
            self.sprite.add(self.void_sprite_group)

        # Set correct sprites for start and end tile
        elif self.tile_type in (self.TYPE_START, self.TYPE_END):
            self.sprite = self.floor_sprites[2][0]

        # Set correct sprite for door tiles
        elif self.tile_type is self.TYPE_DOOR:
            self.sprite = self.door_sprite

        if self.sprite:
            self.sprite.set_pos((self.x * self.tile_size, self.y * self.tile_size))
            if self.tile_type == self.TYPE_DOOR:
                self.sprite.add(self.door_sprite_group)
            else:
                self.sprite.add(self.maze_sprite_group)

    def update_sprite(self):
        self.sprite.kill()
        self.set_sprite()

    # Get the neighbours that are floor tiles for setting the sprite with the correct floor connections
    def floor_neighbours(self):
        floor_neighbours = {}
        for key, neighbour in self.direct_neighbours.items():
            if neighbour.tile_type in (self.TYPE_FLOOR, self.TYPE_START, self.TYPE_END):
                floor_neighbours[key] = neighbour
        return floor_neighbours

    def update_type(self, tile_type):
        self.tile_type = tile_type

    def f_score(self):
        return self.g_score + self.h_score

    def reset_pathfinding(self):
        self.g_score = 0
        self.is_seen = False
        self.is_visited = False

    def __lt__(self, other):
        return self.f_score() < other.f_score()

    def __repr__(self):
        return "(%s, %s)" % (self.x, self.y)
