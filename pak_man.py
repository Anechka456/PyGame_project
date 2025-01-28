import pygame
from load_image import load_image

size = width, height = 900, 800
FPS = 10

MAPS_DIR = "maps"
TITLE_SIZE = 32
ENEMY_EVENT_TYPE = 1


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, group1, group2):
        super().__init__(group1, group2)
        self.image = pygame.Surface((5, 5))
        self.image.fill((250, 210, 1))
        self.rect = pygame.Rect(x * TITLE_SIZE + TITLE_SIZE // 2 + 50, y * TITLE_SIZE + TITLE_SIZE // 2, 5, 5)
        self.rect.x = x * TITLE_SIZE + TITLE_SIZE // 2 + 50
        self.rect.y = y * TITLE_SIZE + TITLE_SIZE // 2


class Labyrinth:
    def __init__(self, filename, free_tile, finish_tile):
        self.map = []
        with open(f"{MAPS_DIR}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TITLE_SIZE
        self.free_tiles = free_tile
        self.finish = finish_tile

    def render(self, screen):
        colors = {0: (0, 0, 0), 1: (0, 0, 255), 2: (50, 50, 50)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size + 50, y * self.tile_size, self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

    def find_path_step(self, start, target):
        INF = 1000
        x, y = start
        distance = [[INF] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        prev = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 <= next_y < self.height and self.is_free((next_x, next_y)) and \
                        distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y


class Hero(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.x, self.y = position
        self.rect = pygame.Rect(self.x * TITLE_SIZE + TITLE_SIZE // 2 + 50, self.y * TITLE_SIZE + TITLE_SIZE // 2,
                                TITLE_SIZE, TITLE_SIZE)
        self.rect.x = self.x * TITLE_SIZE + TITLE_SIZE // 2 + 50
        self.rect.y = self.y * TITLE_SIZE + TITLE_SIZE // 2

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position
        self.rect.x = self.x * TITLE_SIZE + TITLE_SIZE // 2 + 50
        self.rect.y = self.y * TITLE_SIZE + TITLE_SIZE // 2

    def render(self, screen):
        center = self.x * TITLE_SIZE + TITLE_SIZE // 2 + 50, self.y * TITLE_SIZE + TITLE_SIZE // 2
        pygame.draw.circle(screen, (255, 255, 0), center, TITLE_SIZE / 2)


class Enemy:
    def __init__(self, position):
        self.x, self.y = position
        self.delay = 200
        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center = self.x * TITLE_SIZE + TITLE_SIZE // 2 + 50, self.y * TITLE_SIZE + TITLE_SIZE // 2
        pygame.draw.circle(screen, (255, 0, 0), center, TITLE_SIZE / 2)


class Game:
    def __init__(self, labyrinth, hero, enemy1, enemy2):
        self.labyrinth = labyrinth

        self.hero = hero
        self.enemy1 = enemy1
        self.enemy2 = enemy2

    def render(self, screen):
        self.hero.render(screen)
        self.enemy1.render(screen)
        self.enemy2.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
        if self.labyrinth.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))

    def move_enemy(self):
        next_position1 = self.labyrinth.find_path_step(self.enemy1.get_position(), self.hero.get_position())
        next_position2 = self.labyrinth.find_path_step(self.enemy2.get_position(), self.hero.get_position())

        self.enemy1.set_position(next_position1)
        self.enemy2.set_position(next_position2)

    def check_win(self):
        return self.labyrinth.get_tile_id(self.hero.get_position()) == 2

    def check_los(self, enemy):
        return self.hero.get_position() == enemy.get_position()


def show_message(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, 1, (50, 70, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    food_sprites = pygame.sprite.Group()

    points_food = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1),
                   (1, 2), (1, 3), (1, 4)]
    for i in points_food:
        Food(i[0], i[1], all_sprites, food_sprites)

    labyrinth = Labyrinth("simple_map2.txt", [0, 2], 2)
    hero = Hero((19, 17), all_sprites)
    enemy1 = Enemy((7, 1))
    enemy2 = Enemy((12, 12))
    game = Game(labyrinth, hero, enemy1, enemy2)

    clock = pygame.time.Clock()
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ENEMY_EVENT_TYPE and not game_over:
                game.move_enemy()
        if not game_over:
            game.update_hero()
        pygame.sprite.spritecollide(hero, food_sprites, True)
        screen.fill((0, 0, 0))
        labyrinth.render(screen)
        food_sprites.draw(screen)
        game.render(screen)
        if game.check_win():
            game_over = True
            show_message(screen, 'You win')
        if game.check_los(enemy1) or game.check_los(enemy2):
            game_over = True
            show_message(screen, 'You lose')
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
