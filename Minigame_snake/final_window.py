import sqlite3
import sys

import pygame

import map


def finding_best_score():
    con = sqlite3.connect("data/snake_score")
    cur = con.cursor()
    result = cur.execute("""SELECT max(score) FROM allScore""").fetchone()[0]
    con.close()
    if result:
        return result


def adding_score(score):
    con = sqlite3.connect("data/snake_score")
    cur = con.cursor()
    cur.execute(f"""INSERT INTO allScore(score) VALUES({score})""")
    con.commit()


class FinalWindowSnake:
    def __init__(self, score):
        pygame.init()
        width, height = 900, 800
        self.screen = pygame.display.set_mode((width, height))

        # Цвета
        self.background_color = (113, 152, 103)
        self.text_color = (32, 51, 25)
        self.button_color = (33, 94, 33)

        # Шрифт
        self.font = pygame.font.SysFont('impact', 33)  # Шрифт для кнопок
        self.title_font = pygame.font.SysFont('impact', 100)  # Шрифт для заголовка
        self.message_font = pygame.font.SysFont('impact', 60)  # Шрифт для результата

        # Кнопки
        button_width, button_height = 200, 60
        self.try_again_button = pygame.Rect((150, height // 2 + button_height * 2),
                                            (button_width, button_height))
        self.exit_button = pygame.Rect((550, height // 2 + button_height * 2),
                                       (button_width, button_height))

        self.score = score
        adding_score(score)

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
        title_text = self.title_font.render('Snake Game', True, self.text_color)  # Заголовок
        title_rect = title_text.get_rect(center=(450, 200))
        self.screen.blit(title_text, title_rect)

    def draw_score(self):
        # текущий результат
        score_text = self.message_font.render(f'Score: {self.score}', True, self.text_color)
        score_rect = score_text.get_rect(center=(450, 430))
        self.screen.blit(score_text, score_rect)

        # лучший результат
        best_score_text = self.message_font.render(f'Best score: {finding_best_score()}', True, self.text_color)
        best_score_rect = best_score_text.get_rect(center=(450, 350))
        self.screen.blit(best_score_text, best_score_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.try_again_button.collidepoint(event.pos):
                        self.running = False
                    elif self.exit_button.collidepoint(event.pos):
                        map.Map()

            self.screen.fill(self.background_color)
            self.draw_title()
            self.draw_score()
            self.draw_buttons()
            pygame.display.flip()
