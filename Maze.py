from Tile import Tile
from Spritesheet import *
import random


class Maze:
    def __init__(self, width, height):
        if width % 2 is 0:
            width += 1
        if height % 2 is 0:
            height += 1

        # Tilemap heavily inspired by "Dungeon Tilemap" by Michele Bucelli https://opengameart.org/users/buch?page=2
        spritesheet = SpriteSheet("assets/png/tilemap.png")
        self.sprites = {
            "Floor": Sprite(spritesheet, (64, 48, 16, 16)),
            "Wall": Sprite(spritesheet, (48, 48, 16, 16))
        }
        self.maze_sprite_list = pygame.sprite.Group()
        self.width = width
        self.height = height
        self.grid = [[Tile(x, y, Tile.TYPE_WALL, self.sprites["Wall"]) for y in range(height)] for x in range(width)]
        self.start = (2*int(random.uniform(0, self.width//2))+1, 0)
        self.end = (2*int(random.uniform(0, self.width//2))+1, height-1)
        self.set_neighbours()
        self.generate_maze()

    def set_neighbours(self):
        for x in range(1, self.width, 2):
            for y in range(1, self.height, 2):
                grid_tile = self.grid[x][y]
                if y > 1:
                    grid_tile.neighbours['up'] = (self.grid[x][y-1], self.grid[x][y-2])
                if x < self.width-2:
                    grid_tile.neighbours['right'] = (self.grid[x+1][y], self.grid[x+2][y])
                if y < self.height-2:
                    grid_tile.neighbours['down'] = (self.grid[x][y+1], self.grid[x][y+2])
                if x > 1:
                    grid_tile.neighbours['left'] = (self.grid[x-1][y], self.grid[x-2][y])

    def generate_maze(self):
        self.grid[self.start[0]][self.start[1]].set_type(Tile.TYPE_EMPTY)
        neighbours = self.grid[self.start[0]][1].possible_neighbours()
        random.shuffle(neighbours)
        for neighbour in neighbours:
            if neighbour[1].tile_type is Tile.TYPE_WALL:
                self.do_step(neighbour)

    def do_step(self, tile):
        tile[0].set_type(Tile.TYPE_EMPTY, self.sprites["Floor"])
        tile[1].set_type(Tile.TYPE_EMPTY, self.sprites["Floor"])
        neighbours = tile[1].possible_neighbours()
        random.shuffle(neighbours)
        if len(neighbours) is 0:
            return
        for neighbour in neighbours:
            if neighbour[1].tile_type is Tile.TYPE_WALL:
                self.do_step(neighbour)

    def print_grid(self):
        print('\n'.join(''.join(str(tile.tile_type) for tile in row) for row in self.grid))
