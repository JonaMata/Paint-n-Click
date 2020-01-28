from Riddle import Riddle
from Spritesheet import Sprite


class Tile(object):
    TYPE_EMPTY = ' '
    TYPE_WALL = '#'
    TYPE_DOOR = '|'

    def __init__(self, x, y, tile_type, spritesheet, sprite_group, tile_scale):
        self.sprites = {
            Tile.TYPE_WALL: Sprite(spritesheet, (64, 48, 16, 16), scale=tile_scale),
            Tile.TYPE_EMPTY: Sprite(spritesheet, (64, 0, 16, 16), scale=tile_scale)
        }
        self.x = x
        self.y = y
        self.sprite_group = sprite_group
        self.tile_type = tile_type
        self.sprite = self.sprites[tile_type]
        self.sprite.set_pos((x*self.sprite.size[0], y*self.sprite.size[1]))
        self.sprite.add(sprite_group)
        self.neighbours = {}

        if tile_type is self.TYPE_DOOR:
            self.riddle = Riddle()

    def possible_neighbours(self):
        possible = []
        for neighbour in self.neighbours.values():
            if neighbour[1].tile_type is self.TYPE_WALL:
                possible.append(neighbour)
        return possible

    def update_type(self, tile_type):
        self.tile_type = tile_type
        if tile_type is self.TYPE_EMPTY:
            self.sprite.remove(self.sprite_group)

