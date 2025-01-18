import sys

import pygame

from load_image import load_image
from map import Map


class StartWindow:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode((size[0], size[1]))
        pygame.display.set_caption("Better together")
        icon = load_image("images/icon.jpg")
        pygame.display.set_icon(icon)
        self.font = pygame.font.SysFont('impact', 80)
        self.button_font = pygame.font.SysFont('impact', 39)

        self.start_button = pygame.Rect(width / 2 - width / 2 / 4, height / 2, width / 4, height / 8)
        self.title_game = "Better together"

    def draw(self):

        # Рисуем овальный фон вокруг кнопки
        pygame.draw.ellipse(self.screen, (0, 0, 150), self.start_button.inflate(40, 40))
        pygame.draw.ellipse(self.screen, (0, 0, 200), self.start_button.inflate(20, 20))
        pygame.draw.ellipse(self.screen, (0, 0, 255), self.start_button.inflate(0, 0))
        button_text = self.button_font.render("НАЧАТЬ ИГРУ", True, (255, 255, 255))
        w, h = button_text.get_width(), button_text.get_height()
        self.screen.blit(button_text,
                         (self.start_button.x + width / 8 - w / 2, self.start_button.y + height / 16 - h / 2))

        # Отображаем текст
        title_game = self.font.render(self.title_game, True, (255, 255, 255))

        self.screen.blit(title_game, (width // 2 - title_game.get_width() // 2, 100))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.start_button.collidepoint(event.pos):
                            Map()

            self.draw()


pygame.init()
size = width, height = 900, 800
screen = pygame.display.set_mode(size)

StartWindow(size).run()
pygame.quit()
