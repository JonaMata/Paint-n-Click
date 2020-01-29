from Riddle import Riddle
from Spritesheet import Sprite


class Tile(object):
    TYPE_FLOOR = ' '
    TYPE_WALL = '#'
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
            0: Sprite(spritesheet, (64, 0, 16, 16), scale=tile_scale),
            1: Sprite(spritesheet, (64, 0, 16, 16), scale=tile_scale),
            2: Sprite(spritesheet, (64, 0, 16, 16), scale=tile_scale),
            3: Sprite(spritesheet, (64, 0, 16, 16), scale=tile_scale),
            4: Sprite(spritesheet, (64, 0, 16, 16), scale=tile_scale)
        }
        self.x = x
        self.y = y
        self.sprite_group = sprite_group
        self.tile_type = self.TYPE_WALL
        self.sprite = self.wall_sprite
        self.sprite.set_pos((x*self.sprite.size[0], y*self.sprite.size[1]))
        self.sprite.add(sprite_group)
        self.step_neighbours = {}
        self.direct_neighbours = {}
        self.riddle = None

    def possible_stop_neighbours(self):
        possible = []
        for neighbour in self.step_neighbours.values():
            if neighbour[1].tile_type is self.TYPE_WALL:
                possible.append(neighbour)
        return possible

    def set_sprite(self):
        if self.tile_type is self.TYPE_FLOOR:
            floor_neighbours = {}
            for key, neighbour in self.direct_neighbours:
                if neighbour.tile_type in (self.TYPE_FLOOR, self.TYPE_START, self.TYPE_END):
                    floor_neighbours[key] = neighbour

            floor_amount = len(floor_neighbours)
            floor_direction = min(floor_neighbours.keys())

            if floor_amount is 1:
                # Single floor
                return
            elif floor_amount is 2:
                if sum(floor_neighbours.keys()) in (180, 360):
                    # Straight line floor
                    return
                else:
                    # Corner floor
                    return
            elif floor_amount is 3:
                # T-split floor
                return
            elif floor_amount is 4:
                # 4-way floor
                return

    def update_type(self, tile_type):
        self.tile_type = tile_type
        if tile_type in (self.TYPE_FLOOR, self.TYPE_START, self.TYPE_END):
            self.sprite.remove(self.sprite_group)
