import bisect

from Tile import Tile
from Spritesheet import *
import random


class Maze(object):
    def __init__(self, width, height, size):
        if width % 2 is 0:
            width += 1
        if height % 2 is 0:
            height += 1

        # Tilemap heavily inspired by "Dungeon Tilemap" by Michele Bucelli https://opengameart.org/users/buch?page=2
        spritesheet = SpriteSheet("assets/png/tilemap.png")
        self.maze_sprite_group = pygame.sprite.Group()
        self.void_sprite_group = pygame.sprite.Group()
        self.door_sprite_group = pygame.sprite.Group()
        self.width = width
        self.height = height
        self.tile_scale = (size[0] / width / 16)
        self.grid = [[Tile(x, y, spritesheet, self.maze_sprite_group, self.void_sprite_group, self.door_sprite_group, self.tile_scale) for y in range(self.height)] for x in range(self.width)]
        self.start = self.grid[2*int(random.uniform(0, self.width//2))+1][0]
        self.end = self.grid[2*int(random.uniform(0, self.width//2))+1][height-1]
        self.set_neighbours()
        self.generate_maze()

        path = self.find_best_path()
        while path is not None:
            path.remove(self.start)
            path.remove(self.end)
            door_tile = path[int(random.uniform(0, len(path)))]
            door_tile.tile_type = Tile.TYPE_DOOR
            path = self.find_best_path()

        self.set_sprites()
        self.render_console()

    def set_neighbours(self):
        # Set step_neighbours
        for x in range(1, self.width, 2):
            for y in range(1, self.height, 2):
                grid_tile = self.grid[x][y]
                if y > 1:
                    grid_tile.step_neighbours[Tile.DIRECTION_UP] = (self.grid[x][y - 1], self.grid[x][y - 2])
                if x < self.width-2:
                    grid_tile.step_neighbours[Tile.DIRECTION_RIGHT] = (self.grid[x + 1][y], self.grid[x + 2][y])
                if y < self.height-2:
                    grid_tile.step_neighbours[Tile.DIRECTION_DOWN] = (self.grid[x][y + 1], self.grid[x][y + 2])
                if x > 1:
                    grid_tile.step_neighbours[Tile.DIRECTION_LEFT] = (self.grid[x - 1][y], self.grid[x - 2][y])

        # Set direct neighbours
        for x in range(self.width):
            for y in range(self.height):
                grid_tile = self.grid[x][y]
                if y > 0:
                    grid_tile.direct_neighbours[Tile.DIRECTION_UP] = self.grid[x][y-1]
                if x < self.width-1:
                    grid_tile.direct_neighbours[Tile.DIRECTION_RIGHT] = self.grid[x+1][y]
                if y < self.height-1:
                    grid_tile.direct_neighbours[Tile.DIRECTION_DOWN] = self.grid[x][y+1]
                if x > 1:
                    grid_tile.direct_neighbours[Tile.DIRECTION_LEFT] = self.grid[x-1][y]

    def set_h_scores(self):
        for row in self.grid:
            for tile in row:
                tile.h_score = abs(tile.x - self.end[0]) + abs(tile.y - self.end[1])

    def reset_pathfinding(self):
        for row in self.grid:
            for tile in row:
                tile.reset_pathfinding()

    def generate_maze(self):
        self.start.update_type(Tile.TYPE_START)
        self.end.update_type(Tile.TYPE_END)
        neighbours = self.grid[self.start.x][1].possible_stop_neighbours()
        random.shuffle(neighbours)
        for neighbour in neighbours:
            if neighbour[1].tile_type is Tile.TYPE_VOID:
                self.do_generate_step(neighbour)

        destroyable_void_tiles = []
        for row in self.grid[1:len(self.grid)-2]:
            for tile in row[1:len(row)-2]:
                if tile.tile_type is Tile.TYPE_VOID and len(tile.floor_neighbours()) == 2 and sum(tile.floor_neighbours().keys()) % 2 == 0:
                    destroyable_void_tiles.append(tile)

        for i in range(10):
            destroyed_void_tile = destroyable_void_tiles.pop(int(random.uniform(0, len(destroyable_void_tiles))))
            destroyed_void_tile.tile_type = Tile.TYPE_FLOOR

    def do_generate_step(self, tile):
        tile[0].update_type(Tile.TYPE_FLOOR)
        tile[1].update_type(Tile.TYPE_FLOOR)
        neighbours = tile[1].possible_stop_neighbours()
        random.shuffle(neighbours)
        if len(neighbours) is 0:
            return
        for neighbour in neighbours:
            if neighbour[1].tile_type is Tile.TYPE_VOID:
                self.do_generate_step(neighbour)

    def find_best_path(self):
        self.reset_pathfinding()
        self.start.g_score = 0
        self.start.is_seen = True
        open_list = [self.start]
        current_tile = None

        while len(open_list) > 0:
            current_tile = open_list.pop()
            current_tile.is_visited = True
            if current_tile is self.end:
                break
            else:
                for neighbour in current_tile.direct_neighbours.values():
                    if neighbour.tile_type in (Tile.TYPE_FLOOR, Tile.TYPE_END):
                        if not neighbour.is_seen:
                            neighbour.g_score = current_tile.g_score+1
                            neighbour.is_seen = True
                            neighbour.parent = current_tile
                            bisect.insort(open_list, neighbour)
                        else:
                            if neighbour.f_score() > current_tile.f_score()+1:
                                if neighbour in open_list:
                                    open_list.remove(neighbour)
                                neighbour.g_score = current_tile.g_score+1
                                neighbour.parent = current_tile
                                neighbour.is_seen = True
                                bisect.insort(open_list, neighbour)

        if current_tile is self.end:
            path_list = []
            while current_tile is not None:
                path_list.insert(0, current_tile)
                current_tile = current_tile.parent
            return path_list

    def set_sprites(self):
        # Set tile sprites
        for row in self.grid:
            for tile in row:
                tile.set_sprite()

    def render_console(self):
        print('\n'.join(''.join(str(tile.tile_type) for tile in row) for row in self.grid))

    def render(self, screen):
        self.maze_sprite_group.draw(screen)
        self.door_sprite_group.draw(screen)
        for door in self.door_sprite_group:
            door.render_riddle(screen)

    def update(self, drawing_camera):
        for x in range(1, self.width):
            for y in range(1, self.height):
                grid_tile = self.grid[x][y]
                if grid_tile.tile_type == grid_tile.TYPE_DOOR:
                    grid_tile.sprite.update(drawing_camera)
                    if grid_tile.sprite.is_open:
                        grid_tile.tile_type = grid_tile.TYPE_FLOOR
                        grid_tile.update_sprite()
                        for key, neighbour in grid_tile.direct_neighbours.items():
                            neighbour.update_sprite()

    def collision(self, character):
        collided_tiles = pygame.sprite.spritecollide(character, self.void_sprite_group, 0, collide_hitbox)
        if collided_tiles:
            character.collide(collided_tiles[-1])
        collided_doors = pygame.sprite.spritecollide(character, self.door_sprite_group, 0, collide_hitbox)
        if collided_doors:
            collided_doors[-1].collide()
