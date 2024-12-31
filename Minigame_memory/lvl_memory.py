import sys

import pygame

import Minigame_memory.memory


class LevelWindow:
    def __init__(self):
        pygame.init()

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
                                    Minigame_memory.memory.memory(self.screen, 2)
                                if button['text'] == '2 уровень':
                                    self.running = False
                                    Minigame_memory.memory.memory(self.screen, 4)
                                if button['text'] == '3 уровень':
                                    self.running = False
                                    Minigame_memory.memory.memory(self.screen, 6)

            pygame.display.flip()


def play_memory():
    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        LevelWindow()
        pygame.display.flip()
