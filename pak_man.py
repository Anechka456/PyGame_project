import pygame

size = width, height = 480, 480
FPS = 15

MAPS_DIR = "maps"
TITLE_SIZE = 32


class laberint:
    def __init__(self, filename, free_tile, finish_tile):
        self.map = []
        with open(f"{MAPS_DIR}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.heihgt = len(self.map)
        self.wigth = len(self.map[0])
        self.tile_size = TITLE_SIZE
        self.free_tiles = free_tile
        self.finish = finish_tile

    def render(self, screen):
        colors = {0: (0, 0, 0), 1: (120, 120, 120), 2: (50, 50, 50)}
        for y in range(self.heihgt):
            for x in range(self.wigth):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)
    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)

    labirint = laberint("simple_map.txt", [0, 2], 2)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        labirint.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
