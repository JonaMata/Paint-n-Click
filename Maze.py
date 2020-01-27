from Tile import Tile


class Maze:
    def __init__(self, width, height):
        if width % 2 is 0:
            width += 1
        if height % 2 is 0:
            height += 1

        self.grid = [[Tile(Tile.TYPE_EMPTY)] * height] * width

    def print_grid(self):
        print('\n'.join(', '.join(str(tile.tile_type) for tile in column) for column in self.grid))
