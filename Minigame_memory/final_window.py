import sys

import pygame

import Minigame_memory.memory


class FinalWindowMemory:
    def __init__(self, lvl, text):
        pygame.init()
        width, height = 900, 800
        self.screen = pygame.display.set_mode((width, height))

        # Цвета
        self.background_color = (66, 52, 49)
        self.text_color = (255, 204, 153)
        self.button_color = (255, 153, 51)

        # Шрифт
        self.font = pygame.font.SysFont('impact', 33)  # Шрифт для кнопок
        self.title_font = pygame.font.SysFont('impact', 100)  # Шрифт для заголовка
        self.message_font = pygame.font.SysFont('impact', 60)  # Шрифт для сообщения

        # Кнопки
        button_width, button_height = 200, 60
        self.try_again_button = pygame.Rect((150, height // 2 + button_height),
                                            (button_width, button_height))
        self.exit_button = pygame.Rect((550, height // 2 + button_height),
                                       (button_width, button_height))

        self.lvl = lvl
        self.text = text

        self.running = True
        self.run()

    def draw_buttons(self):
        pygame.draw.rect(self.screen, self.button_color, self.try_again_button)
        pygame.draw.rect(self.screen, self.button_color, self.exit_button)

        try_again_text1 = self.font.render('Попробовать', True, self.text_color)
        try_again_text2 = self.font.render('снова', True, self.text_color)
        exit_text = self.font.render('Выход', True, self.text_color)

        self.screen.blit(try_again_text1, (self.try_again_button.x + 8, self.try_again_button.y - 5))
        self.screen.blit(try_again_text2, (self.try_again_button.x + 60, self.try_again_button.y + 20))
        self.screen.blit(exit_text, (self.exit_button.x + 50, self.exit_button.y + 10))

    def draw_title(self):
        title_text = self.title_font.render('Game Memory', True, self.text_color)  # Заголовок
        title_rect = title_text.get_rect(center=(450, 200))
        self.screen.blit(title_text, title_rect)

    def draw_message(self):
        message_text = self.message_font.render(self.text, True, self.text_color)  # Сообщение
        title_rect = message_text.get_rect(center=(450, 350))
        self.screen.blit(message_text, title_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.try_again_button.collidepoint(event.pos):
                        Minigame_memory.memory.memory(self.screen, self.lvl)
                        self.running = False
                    elif self.exit_button.collidepoint(event.pos):
                        self.running = False

            self.screen.fill(self.background_color)
            self.draw_title()
            self.draw_message()
            self.draw_buttons()
            pygame.display.flip()
