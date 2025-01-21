import random
import sys

import pygame

from Minigame_space import final_window
from load_image import load_image

all_sprites = pygame.sprite.Group()
alien_sprites = pygame.sprite.Group()
platforms_sprites = pygame.sprite.Group()


def check_win():
    if not alien_sprites:
        cleaning_sprites()
        final_window.FinalWindowSpace('Вы выйграли!')


def game_over():
    cleaning_sprites()
    final_window.FinalWindowSpace('К сожалению вы проиграли!')


def cleaning_sprites():
    all_sprites.empty()
    alien_sprites.empty()
    platforms_sprites.empty()


class Alien(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("data_space/alien.png"), (100, 100))

    def __init__(self, coord):
        super().__init__(all_sprites, alien_sprites)
        self.image = Alien.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = 1
        self.speed = 10

    def update(self):
        if pygame.sprite.spritecollideany(self, platforms_sprites):
            game_over()

        if self.rect.x >= 850:
            self.direction = -1
            self.rect.y += 50
        elif self.rect.x <= 0:
            self.direction = 1
            self.rect.y += 50
        self.rect.x += self.speed * self.direction


class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("data_space/bullet.png"), (50, 70))

    def __init__(self, coord):
        super().__init__(all_sprites)
        self.image = Bullet.image
        self.rect = self.image.get_rect(topleft=(coord[0] + 125, coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y -= 5
        for i in alien_sprites:
            if pygame.sprite.collide_mask(self, i):
                self.kill()
                i.kill()


class Spaceship(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("data_space/spaceship.png"), (300, 300))

    def __init__(self, coord):
        super().__init__(all_sprites)
        self.image = Spaceship.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        self.speed = 10

    def update(self, *args):
        keys = pygame.key.get_pressed()

        # A -> Left; D -> Right
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed


class Platforms(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, platforms_sprites)
        self.image = pygame.Surface((900, 5))
        self.image.fill((150, 0, 0))
        self.rect = pygame.Rect(x, y, 900, 5)
        self.rect.x = x
        self.rect.y = y


class Space:
    def __init__(self):
        self.spaceship = Spaceship((320, 500))
        for i in range(20):
            Alien((random.randint(0, 900), 20))
        Platforms(0, 501)

        self.background = load_image('data_space/background.png')

        self.run()

    def run(self):
        pygame.init()
        size = width, height = 900, 800
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        fps = 60
        pygame.display.set_caption('Space Game')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Bullet((self.spaceship.rect.x, 480))
                    self.spaceship.update(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Bullet((self.spaceship.rect.x, 480))

            all_sprites.update()

            screen.blit(self.background, (0, 0))
            all_sprites.draw(screen)
            check_win()
            pygame.display.flip()
            clock.tick(fps)


def play_space():
    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        Space()
        pygame.display.flip()
