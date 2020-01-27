from Riddle import Riddle


class Tile:
    TYPE_EMPTY = 0
    TYPE_WALL = 1
    TYPE_DOOR = 2

    def __init__(self, tile_type):
        self.tile_type = tile_type

        if tile_type is self.TYPE_DOOR:
            self.riddle = Riddle()
