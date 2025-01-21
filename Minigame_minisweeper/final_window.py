import pygame
import sys


class FinalWindowSweeper:
    def __init__(self, indicator, lvl, time):
        pygame.init()

        self.size = width, height = 900, 800
        self.background_color = (99, 69, 48)
        self.text_color = (243, 179, 145)
        self.button_color = (168, 101, 64)
        self.screen = pygame.display.set_mode((width, height))
        self.font_title = pygame.font.SysFont("impact", 80)
        self.font = pygame.font.SysFont("impact", 50)
        self.button_font = pygame.font.SysFont("impact", 40)

        self.id = indicator
        self.lvl = lvl
        self.time = time
        self.running = True
        self.run()

    def draw_text(self, text, font, color, x, y):
        dtext = font.render(text, True, color)
        dtextrect = dtext.get_rect()
        dtextrect.topleft = (x, y)
        self.screen.blit(dtext, dtextrect)

    def draw_button(self, text, x, y, width, height):
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, self.button_color, button_rect)
        self.draw_text(text, self.button_font, self.text_color, x + 15, y)
        return button_rect

    def run(self):
        # Основной цикл
        while self.running:
            self.screen.fill(self.background_color)

            if self.id == 1:
                self.draw_text('Game over', self.font_title, self.text_color, 270, 270)
                self.draw_text('Вы наткнулись на бомбу...', self.font, self.text_color, 180, 400)
            elif self.id == 2:
                self.draw_text('Поздравляем!', self.font_title, self.text_color, 210, 270)
                self.draw_text('Вы открыли все', self.font, self.text_color, 270, 400)
                self.draw_text('безопасные клетки!', self.font, self.text_color, 230, 450)

            self.draw_text("Game Minisweeper", self.font_title, self.text_color, 140, 80)
            self.draw_text(f"Уровень: {self.lvl}", self.font, self.text_color, 335, 530)
            minutes = str(self.time // 60).rjust(2, '0')
            seconds = str(self.time % 60).rjust(2, '0')
            self.draw_text(f"Время: {minutes}:{seconds}", self.font, self.text_color,
                           305, 580)

            # Рисуем кнопки
            exit_button = self.draw_button("х", 830, 20, 50, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        if exit_button.collidepoint(event.pos):
                            self.running = False
            pygame.display.flip()
