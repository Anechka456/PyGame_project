import sys

import pygame

from Minigame_memory.lvl_memory import play_memory
from Minigame_minisweeper.lvl_minisweeper import play_sweeper
from Minigame_snake.snake import play_snake
from Minigame_space.space import play_space
from Minigame_pacman.pak_man import play_pacman
from load_image import load_image

pygame.mixer.init()

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
barrier_group = pygame.sprite.Group()
interactive_points = pygame.sprite.Group()
nature_points = pygame.sprite.Group()

tile_width = tile_height = 50


def window_snake():
    cleaning_sprites()
    play_snake()


def window_pacman():
    cleaning_sprites()
    play_pacman()


def window_sweeper():
    cleaning_sprites()
    play_sweeper()


def window_memory():
    cleaning_sprites()
    play_memory()


def window_space():
    cleaning_sprites()
    play_space()


def cleaning_sprites():
    """Функция очищает группы спрайтов"""
    all_sprites.empty()
    tiles_group.empty()
    player_group.empty()
    barrier_group.empty()
    interactive_points.empty()
    nature_points.empty()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


class MiniGameSnake(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("images/house.png"), (250, 300))

    def __init__(self, group, coord):
        super().__init__(group, all_sprites)
        self.image = MiniGameSnake.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class MiniGamePacMan(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("images/school.png"), (300, 300))

    def __init__(self, group, coord):
        super().__init__(group, all_sprites)
        self.image = MiniGamePacMan.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class MiniGameMemory(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("images/educational_institution.png"), (500, 400))

    def __init__(self, group, coord):
        super().__init__(group, all_sprites)
        self.image = MiniGameMemory.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class MiniGameSweeper(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("images/army.png"), (300, 300))

    def __init__(self, group, coord):
        super().__init__(group, all_sprites)
        self.image = MiniGameSweeper.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class MiniGameSpace(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("images/rocket.png"), (430, 500))

    def __init__(self, group, coord):
        super().__init__(group, all_sprites)
        self.image = MiniGameSpace.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class Nature(pygame.sprite.Sprite):
    nature_images = {
        'tree1': pygame.transform.scale(load_image('images/tree1.png'), (200, 200)),
        'tree2': pygame.transform.scale(load_image('images/tree2.png'), (150, 200)),
        'tree3': pygame.transform.scale(load_image('images/tree3.png'), (250, 250)),
        'field': pygame.transform.scale(load_image('images/field.png'), (500, 400))

    }

    def __init__(self, tile_type, coord):
        super().__init__(nature_points, all_sprites)
        self.image = Nature.nature_images[tile_type]
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class Tile(pygame.sprite.Sprite):
    tile_images = {
        'wall': pygame.transform.scale(load_image('images/grass.png'), (50, 50)),
        'empty1': pygame.transform.scale(load_image('images/grass.png'), (50, 50)),
        'empty2': pygame.transform.scale(load_image('images/path.png'), (50, 50))

    }

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = Tile.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, width, height):
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)


class Player(pygame.sprite.Sprite):
    player_image = pygame.transform.scale(load_image('images/character.png'), (35, 70))
    sound_walking = pygame.mixer.Sound('data/images/walking.wav')

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = Player.player_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.cycle_number = 0
        self.animation_timer = 0
        self.speed = 400
        Player.sound_walking.play(-1)

    def update(self, *args):
        Player.sound_walking.set_volume(1)
        old_x = self.rect.x
        old_y = self.rect.y

        # W -> Up; S -> Down; A -> Left; D -> Right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.cycle_number % 2 == 0:
                self.image = pygame.transform.scale(load_image('images/character_left1.png'), (35, 70))
            else:
                self.image = pygame.transform.scale(load_image('images/character_left2.png'), (35, 70))
            self.animation_timer += 1
            self.rect.x -= self.speed / 60
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.cycle_number % 2 == 0:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(load_image('images/character_left1.png'), (35, 70)), True, False)
            else:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(load_image('images/character_left2.png'), (35, 70)), True, False)
            self.animation_timer += 1
            self.rect.x += self.speed / 60
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.cycle_number % 2 == 0:
                self.image = pygame.transform.scale(load_image('images/character_up1.png'), (35, 70))
            else:
                self.image = pygame.transform.scale(load_image('images/character_up2.png'), (35, 70))
            self.animation_timer += 1
            self.rect.y -= self.speed / 60
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.cycle_number % 2 == 0:
                self.image = pygame.transform.scale(load_image('images/character_down1.png'), (35, 70))
            else:
                self.image = pygame.transform.scale(load_image('images/character_down2.png'), (35, 70))
            self.animation_timer += 1
            self.rect.y += self.speed / 60
        else:
            Player.sound_walking.set_volume(0)
            self.image = Player.player_image
            self.animation_timer = 0
            self.cycle_number = 0
            return

        if self.animation_timer % 10 == 0:  # каждые 10 кадров
            self.cycle_number += 1

        # проверка на коллизию
        if pygame.sprite.spritecollideany(self, barrier_group):
            self.rect.x = old_x
            self.rect.y = old_y

        for i in nature_points:
            if pygame.sprite.collide_mask(self, i):
                self.rect.x = old_x
                self.rect.y = old_y


class Map:
    def __init__(self, x, y):
        pygame.display.set_caption("Better together")

        self.x = x
        self.y = y

        # интерактивные точки
        self.coord_interactive_points = [(60, 500), (1380, 0), (1300, 990), (60, 1530), (1200, 1900)]

        # точки деревьев
        coord_tree = [('field', (290, 50)), ('tree1', (80, 80)), ('tree2', (550, 350)), ('tree1', (900, 30)),
                      ('tree3', (1100, 50)), ('tree3', (1100, 700)), ('tree1', (1350, 500)), ('tree2', (730, 250)),
                      ('tree2', (350, 400)), ('tree2', (800, 750)), ('tree2', (60, 1100)), ('tree1', (300, 1200)),
                      ('tree3', (650, 1250)), ('tree1', (1050, 1700)), ('tree3', (1350, 1500)), ('tree3', (200, 2000)),
                      ('tree1', (600, 2200))]
        for i in coord_tree:
            Nature(i[0], i[1])

        self.pac_man = MiniGamePacMan(interactive_points, self.coord_interactive_points[0])
        self.snake = MiniGameSnake(interactive_points, self.coord_interactive_points[1])
        self.sweeper = MiniGameSweeper(interactive_points, self.coord_interactive_points[2])
        self.memory = MiniGameMemory(interactive_points, self.coord_interactive_points[3])
        self.space = MiniGameSpace(interactive_points, self.coord_interactive_points[4])

        self.start()

    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty1', x, y)
                elif level[y][x] == ',':
                    Tile('empty2', x, y)
                elif level[y][x] == '#':
                    wall = Tile('wall', x, y)
                    barrier_group.add(wall)
        new_player = Player(self.x, self.y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y

    def start(self):
        pygame.init()

        size = width, height = 900, 800
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        fps = 60
        camera = Camera(width, height)
        player, level_x, level_y = self.generate_level(load_level('map.txt'))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    player.update(event)

            if pygame.sprite.collide_mask(player, self.memory):
                Player.sound_walking.stop()
                window_memory()
                terminate()

            elif pygame.sprite.collide_mask(player, self.snake):
                Player.sound_walking.stop()
                window_snake()
                terminate()

            elif pygame.sprite.collide_mask(player, self.pac_man):
                Player.sound_walking.stop()
                window_pacman()
                terminate()

            elif pygame.sprite.collide_mask(player, self.sweeper):
                Player.sound_walking.stop()
                window_sweeper()
                terminate()

            elif pygame.sprite.collide_mask(player, self.space):
                Player.sound_walking.stop()
                window_space()
                terminate()

            player.update()
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)
            screen.fill((87, 132, 84))
            tiles_group.draw(screen)
            interactive_points.draw(screen)
            nature_points.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
