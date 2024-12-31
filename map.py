import sys

import pygame

from Minigame_memory.lvl_memory import play_memory
from Minigame_minisweeper.lvl_minisweeper import play_sweeper
from Minigame_snake.snake import play
from load_image import load_image


def window_snake():
    play()


def window_sweeper():
    play_sweeper()


def window_memory():
    play_memory()


class MinigameSnake(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("images/star.png"), (50, 50))

    def __init__(self, group, coord):
        super().__init__(group)
        self.image = MinigameSnake.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class MinigameMemory(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("images/rocket.png"), (200, 200))

    def __init__(self, group, coord):
        super().__init__(group)
        self.image = MinigameMemory.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class MinigameSweeper(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("images/book.png"), (80, 80))

    def __init__(self, group, coord):
        super().__init__(group)
        self.image = MinigameSweeper.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class Players(pygame.sprite.Sprite):
    player_image_bottom = pygame.transform.scale(load_image('images/character.png'), (60, 60))
    player_image_top = pygame.transform.scale(load_image('images/character_up.png'), (60, 60))
    player_image_right = pygame.transform.scale(load_image('images/character_right.png'), (60, 60))
    player_image_left = pygame.transform.scale(load_image('images/character_left.png'), (60, 60))

    def __init__(self, group):
        super().__init__(group)
        self.image = Players.player_image_bottom
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.rect.center = (900 // 2, 800 // 2)
        self.player_speed = 5

    def update(self, *args):
        keys = pygame.key.get_pressed()

        # W -> Up; S -> Down; A -> Left; D -> Right
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.image = Players.player_image_left
            self.rect.x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.image = Players.player_image_right
            self.rect.x += self.player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.image = Players.player_image_top
            self.rect.y -= self.player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.image = Players.player_image_bottom
            self.rect.y += self.player_speed


class Map:
    def __init__(self):
        pygame.init()

        size = width, height = 900, 800
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Adventures with mini")
        icon = load_image("images/icon.jpg")
        pygame.display.set_icon(icon)

        self.background_image = pygame.transform.scale(load_image('images/map.png'), (900, 800))
        self.interactive_points = pygame.sprite.Group()
        self.coord_interactive_points = [(80, 580), (150, 100), (700, 400)]

        self.memory = MinigameMemory(self.interactive_points, self.coord_interactive_points[0])
        self.snake = MinigameSnake(self.interactive_points, self.coord_interactive_points[1])
        self.sweeper = MinigameSweeper(self.interactive_points, self.coord_interactive_points[2])

        self.players_sprite = pygame.sprite.Group()
        self.players = Players(self.players_sprite)

        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if pygame.sprite.collide_mask(self.players, self.memory):
                window_memory()
                self.players.x = 300
                self.players.y = 300
            elif pygame.sprite.collide_mask(self.players, self.snake):
                window_snake()
                self.players.x = 300
                self.players.y = 300
            elif pygame.sprite.collide_mask(self.players, self.sweeper):
                window_sweeper()
                self.players.x = 300
                self.players.y = 300

            self.players_sprite.update()
            # Отрисовка
            self.screen.blit(self.background_image, (0, 0))
            self.players_sprite.draw(self.screen)
            self.interactive_points.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()


Map()
