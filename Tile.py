from Riddle import Riddle


class Tile:
    TYPE_EMPTY = ' '
    TYPE_WALL = '#'
    TYPE_DOOR = '|'

    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.neighbours = {}

        if tile_type is self.TYPE_DOOR:
            self.riddle = Riddle()

    def possible_neighbours(self):
        possible = []
        for neighbour in self.neighbours.values():
            if neighbour.tile_type is self.TYPE_WALL:
                possible.append(neighbour)
        return possible

    def set_type(self, tile_type):
        self.tile_type = tile_type
