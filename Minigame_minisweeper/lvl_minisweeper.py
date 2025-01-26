import random
import sys

import pygame

import map
from Minigame_minisweeper.sweeper import Play
from load_image import load_image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    intro_text = ["В апреле 1950 года Андрияна Григорьевича Николаева",
                  "призвали в ряды Советской Армии.",
                  "Он проходил службу в авиационной",
                  "части на Кавказе.",
                  "Во время службы обучался",
                  "на курсах воздушных стрелков",
                  "при Кировабадском Военно-авиационном ",
                  "училище лётчиков им. Хальзунова.",
                  "Так судьба Андрияна Николаева",
                  "навсегда оказалась связанной с авиацией."
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
        images = pygame.transform.scale(load_image('images_sweeper/uno.png'), (300, 500))
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


class LevelWindow:
    def __init__(self):
        pygame.init()

        self.width, self.height = 900, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game Minisweeper")

        self.background_color = (99, 69, 48)
        self.text_color = (243, 179, 145)

        self.font = pygame.font.SysFont("impact", 80)
        self.button_font = pygame.font.SysFont("impact", 50)

        self.buttons = [
            {"rect": pygame.Rect(100, 200, 700, 100), "text": "1 уровень"},
            {"rect": pygame.Rect(100, 400, 700, 100), "text": "2 уровень"},
            {"rect": pygame.Rect(100, 600, 700, 100), "text": "3 уровень"},
            {"rect": pygame.Rect(830, 20, 50, 50), "text": "X"}
        ]

        self.running = True
        self.run()

    def draw_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, (168, 101, 64), button["rect"])  # Цвет кнопки
            text_surface = self.button_font.render(button["text"], True, self.text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

    def run(self):
        while self.running:
            self.screen.fill(self.background_color)
            self.screen.blit(self.font.render("Game Minisweeper", True, self.text_color), (140, 50))
            self.draw_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos
                        for button in self.buttons:
                            if button["rect"].collidepoint(mouse_pos):
                                # Обработка нажатия кнопки
                                if button['text'] == '1 уровень':
                                    self.running = False
                                    Play(10, 10)
                                elif button['text'] == '2 уровень':
                                    self.running = False
                                    Play(13, 13)
                                elif button['text'] == '3 уровень':
                                    self.running = False
                                    Play(15, 15)
                                elif button['text'] == 'X':
                                    self.running = False
                                    map.Map(1250, 1250)

            pygame.display.flip()


def play_sweeper():
    pygame.init()
    size = width, height = 900, 800
    screen = pygame.display.set_mode(size)
    start_screen(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        LevelWindow()
        pygame.display.flip()
