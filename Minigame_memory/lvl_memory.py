import random
import sys

import pygame

import Minigame_memory.memory
import map
from load_image import load_image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    intro_text = ["После армии Андриян Николаев",
                  "решил продолжить обучение",
                  "и стал курсантом школы воздушных стрелков",
                  "действующей в Черниговском военном училище.",
                  " Отучившись положенный срок,",
                  "грамотный и дисциплинированный",
                  "лётчик попал в Подмосковье.",
                  "Его непосредственным ",
                  "командиром и наставником",
                  "стал легендарный ",
                  "Александр Покрышкин.",
                  "В 1968 году",
                  "ему вручили диплом",
                  "по специальности",
                  "«Лётчик-инженер-космонавт»",
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
        images = pygame.transform.scale(load_image('images_memory/cat.png'), (300, 500))
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
        pygame.mixer.init()
        self.sound_click = pygame.mixer.Sound('data/images/click.mp3')

        self.width, self.height = 900, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game Memory")

        self.background_color = (66, 52, 49)
        self.text_color = (255, 204, 153)

        self.font = pygame.font.SysFont('impact', 80)
        self.button_font = pygame.font.SysFont('impact', 50)

        self.buttons = [
            {"rect": pygame.Rect(100, 200, 700, 100), "text": "1 уровень"},
            {"rect": pygame.Rect(100, 400, 700, 100), "text": "2 уровень"},
            {"rect": pygame.Rect(100, 600, 700, 100), "text": "3 уровень"},
            {"rect": pygame.Rect(830, 20, 50, 50), "text": "X"},
        ]

        self.running = True
        self.run()

    def draw_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, (255, 153, 51), button["rect"])  # Цвет кнопки
            text_surface = self.button_font.render(button["text"], True, self.text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

    def run(self):
        while self.running:
            self.screen.fill(self.background_color)
            self.screen.blit(self.font.render("Game Memory", True, self.text_color), (220, 50))
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
                                    Minigame_memory.memory.memory(self.screen, 2)
                                if button['text'] == '2 уровень':
                                    self.running = False
                                    Minigame_memory.memory.memory(self.screen, 4)
                                if button['text'] == '3 уровень':
                                    self.running = False
                                    Minigame_memory.memory.memory(self.screen, 6)
                                elif button['text'] == 'X':
                                    self.running = False
                                    map.Map(500, 1800)

            pygame.display.flip()


def play_memory():
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
        LevelWindow()
        pygame.display.flip()
