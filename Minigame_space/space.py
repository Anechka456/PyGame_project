import random
import sys

import pygame

from Minigame_space import final_window
from load_image import load_image

# группы спрайтов
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
    """Функция очищает группы спрайтов"""
    all_sprites.empty()
    alien_sprites.empty()
    platforms_sprites.empty()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    intro_text = ["Первый полёт Андрияна Николаева в космос",
                  "состоялся 11 августа 1962 года на корабле «Восток-3».",
                  "Продолжительность полёта составила 4 суток.",
                  "За это время «Восток-3» сумел облететь вокруг Земли 64 раза.",
                  "Это был первый рекорд по длительности полёта.",
                  "2 Второй полёт Андрияна Николаева состоялся",
                  "1 июня 1970 года совместно с космонавтом",
                  "Виталием Севастьяновым на корабле «Восток-9».",
                  "Полет длился 18 суток. Космонавты пробыли",
                  "на орбите 424 часа 59 минут и совершили",
                  "286 оборотов вокруг Земли"
                  ]

    # Создание списка звезд
    stars = []
    for _ in range(200):
        x = random.randint(0, 900)
        y = random.randint(0, 800)
        stars.append((x, y, random.randint(1, 3)))  # (x, y, размер)

    def draw_stars():
        """Функция рисует звезды"""
        for star in stars:
            x, y, size = star
            # Случайное мерцание звезд
            brightness = random.randint(100, 255)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)

    def draw_text():
        """Функция рисует текст"""
        font = pygame.font.SysFont('impact', 30)
        text_coord = 20
        for line in intro_text:
            string_rendered = font.render(line, 1, (102, 0, 255))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def draw_images():
        """Функция вставляет картинку"""
        images = pygame.transform.scale(load_image('data_space/astronaut.png'), (300, 500))
        screen.blit(images, (600, 300))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        screen.fill((0, 0, 0))
        draw_stars()
        draw_text()
        draw_images()
        pygame.display.flip()
        pygame.time.delay(100)  # Задержка для изменения "мерцания"


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
            if self.rect.x > -110:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.x < 710:
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
    size = width, height = 900, 800
    screen = pygame.display.set_mode(size)
    start_screen(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        Space()
        pygame.display.flip()
