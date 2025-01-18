import sys

import pygame

import map
from Minigame_minisweeper.sweeper import Play


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
                    pygame.quit()
                    sys.exit()
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
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        LevelWindow()
        pygame.display.flip()
