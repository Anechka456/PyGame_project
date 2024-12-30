import pygame
import sys


class StartWindow:
    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode((size[0], size[1]))
        pygame.display.set_caption("Игровое окно")
        self.font = pygame.font.Font(None, 30)
        self.button_font = pygame.font.Font(None, 48)

        self.start_button = pygame.Rect(width / 2 - width / 2 / 4, height / 2, width / 4, 100)
        self.title_game = "Better together"

    def draw(self):

        # Рисуем овальный фон вокруг кнопки
        pygame.draw.ellipse(self.screen, (0, 0, 150), self.start_button.inflate(40, 40))
        pygame.draw.ellipse(self.screen, (0, 0, 200), self.start_button.inflate(20, 20))
        pygame.draw.ellipse(self.screen, (0, 0, 255), self.start_button.inflate(0, 0))
        button_text = self.button_font.render("Начать игру", True, (255, 255, 255))
        self.screen.blit(button_text, (self.start_button.x + 15, self.start_button.y + 30))

        # Отображаем текст
        title_game = pygame.font.Font(None, 74).render(self.title_game, True, (255, 255, 255))

        self.screen.blit(title_game, (270, 100))

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
                            running = False

            self.draw()


pygame.init()
size = width, height = 900, 800
screen = pygame.display.set_mode(size)

StartWindow(size).run()
pygame.quit()
