import pygame
import sys
import random

from Minigame_snake.final_window import FinalWindowSnake
from load_image import load_image


class Snake:
    def __init__(self):
        pygame.init()

        self.speed = 0

        self.frame_size_x = 900
        self.frame_size_y = 800

        pygame.display.set_caption('Snake Game')
        self.screen = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.dark_green = pygame.Color(32, 51, 25)
        self.blue = pygame.Color(0, 0, 255)

        self.fps = pygame.time.Clock()

        # змейка
        self.snake_pos = [150, 150]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]

        # яблоко
        self.food_pos = [random.randrange(110, self.frame_size_x - 200),
                         random.randrange(110, self.frame_size_y - 200)]
        food_image = load_image('images_snake/apple.png')
        self.food_image = pygame.transform.scale(food_image, (20, 20))
        self.food_spawn = True

        self.direction = 'RIGHT'
        self.change_to = self.direction

        self.score = 0
        self.running = True
        self.drawing = True
        self.run()

    def show_score(self, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.frame_size_x / 7, 40)
        self.screen.blit(score_surface, score_rect)

    def draw(self):
        self.screen.fill((113, 152, 103))
        image_snake = pygame.transform.scale(load_image('images_snake/snake.png'), (500, 550))
        self.screen.blit(image_snake, (200, 300, 100, 500))
        font = pygame.font.SysFont('impact', 80)
        text = font.render("Press any Key to Restart", True, (0, 0, 0))
        rect = text.get_rect(center=(450, 200))
        self.screen.blit(text, rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Управление кнопками
                elif event.type == pygame.KEYDOWN:
                    if self.drawing:
                        self.drawing = False
                        self.speed = 25
                    else:
                        # W -> Up; S -> Down; A -> Left; D -> Right
                        if event.key == pygame.K_UP or event.key == ord('w'):
                            self.change_to = 'UP'
                        if event.key == pygame.K_DOWN or event.key == ord('s'):
                            self.change_to = 'DOWN'
                        if event.key == pygame.K_LEFT or event.key == ord('a'):
                            self.change_to = 'LEFT'
                        if event.key == pygame.K_RIGHT or event.key == ord('d'):
                            self.change_to = 'RIGHT'
                        if event.key == pygame.K_ESCAPE:
                            pygame.event.post(pygame.event.Event(pygame.QUIT))
            if self.drawing:
                self.draw()
            else:
                # Условия чтобы змейка не могла переместиться в противоположном направлении
                if self.change_to == 'UP' and self.direction != 'DOWN':
                    self.direction = 'UP'
                if self.change_to == 'DOWN' and self.direction != 'UP':
                    self.direction = 'DOWN'
                if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                    self.direction = 'RIGHT'

                # Перемещение змейки
                if self.direction == 'UP':
                    self.snake_pos[1] -= 10
                if self.direction == 'DOWN':
                    self.snake_pos[1] += 10
                if self.direction == 'LEFT':
                    self.snake_pos[0] -= 10
                if self.direction == 'RIGHT':
                    self.snake_pos[0] += 10

                # Рост змейки
                self.snake_body.insert(0, list(self.snake_pos))

                # Проверяем условия столкновения
                if (self.snake_pos[0] <= self.food_pos[0] + 15 <= self.snake_pos[0] + 15 and
                        self.snake_pos[1] <= self.food_pos[1] + 15 <= self.snake_pos[1] + 15):
                    self.score += 1
                    self.food_spawn = False
                else:
                    self.snake_body.pop()  # Удаляем последний рост, если яблоко не съедено

                # Появление яблока
                if not self.food_spawn:
                    self.food_pos = [random.randrange(110, self.frame_size_x - 200),
                                     random.randrange(110, self.frame_size_y - 200)]
                self.food_spawn = True

                # отрисовка
                self.screen.fill((113, 152, 103))
                self.screen.fill((97, 152, 75), (100, 100, self.frame_size_x - 200, self.frame_size_y - 200))
                pygame.draw.rect(self.screen, self.dark_green,
                                 (100, 100, self.frame_size_x - 200, self.frame_size_y - 200),5)
                for pos in self.snake_body:
                    # Snake body
                    pygame.draw.rect(self.screen, self.dark_green, pygame.Rect(pos[0], pos[1], 15, 15))

                # Snake food
                self.screen.blit(self.food_image, (self.food_pos[0], self.food_pos[1], 15, 15))

                # Условия об окончании игры
                if self.snake_pos[0] < 105 or self.snake_pos[0] > self.frame_size_x - 115:
                    self.running = False
                    FinalWindowSnake(self.score)

                if self.snake_pos[1] < 105 or self.snake_pos[1] > self.frame_size_y - 115:
                    self.running = False
                    FinalWindowSnake(self.score)

                for block in self.snake_body[1:]:
                    if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                        self.running = False
                        FinalWindowSnake(self.score)

                self.show_score(self.dark_green, 'impact', 30)
            pygame.display.flip()
            self.fps.tick(self.speed)


def play_snake():
    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        Snake()
        pygame.display.flip()

