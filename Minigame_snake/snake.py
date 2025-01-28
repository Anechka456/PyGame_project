import pygame
import sys
import random

from Minigame_snake.final_window import FinalWindowSnake
from load_image import load_image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    intro_text = ["Родился Андриян Николаев в глухой чувашской",
                  "деревне Шоршелы 5 сентября 1929 года, в обычной крестьянской семье.",
                  "В детские годы говорил на чувашском языке.",
                  "Отец — Григорий Николаевич Николаев (1898—1944)",
                  "конюх в первом колхозе района.",
                  "Мать — Анна Алексеевна Алексеева-Николаева (1900—1987),",
                  "доярка на молочной ферме.",
                  "Поженились в 1922 году, всю жизнь прожили",
                  "в небольшой избе в два окошка.",
                  "Старший брат Иван (1924—2010),",
                  "младший — Пётр, сестра Зинаида."
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
        images = pygame.transform.scale(load_image('images_snake/Andreika.png'), (300, 500))
        screen.blit(images, (550, 300))


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


class Food(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('images_snake/apple.png'), (20, 20))
    def __init__(self, group, coord):
        super().__init__(group)
        self.image = Food.image
        self.rect = self.image.get_rect(topleft=(coord[0], coord[1]))
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class SnakeHead(pygame.sprite.Sprite):
    def __init__(self, group, pos_x, pos_y):
        super().__init__(group)
        self.image = pygame.Surface((15, 15))
        self.rect = pygame.Rect(pos_x, pos_y, 15, 15)


class Snake:
    def __init__(self):
        pygame.init()

        self.speed = 0

        self.frame_size_x = 900
        self.frame_size_y = 800

        pygame.display.set_caption('Snake Game')
        self.screen = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

        # rgb
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.dark_green = pygame.Color(32, 51, 25)
        self.blue = pygame.Color(0, 0, 255)
        self.green = (0, 105, 0)

        self.clock = pygame.time.Clock()
        self.food_sprites = pygame.sprite.Group()
        self.head_sprites = pygame.sprite.Group()

        # змейка
        self.snake_pos = [150, 150]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]

        # яблоко
        self.food_pos = [random.randrange(110, self.frame_size_x - 200),
                         random.randrange(110, self.frame_size_y - 200)]
        self.apple = Food(self.food_sprites, self.food_pos)
        self.food_image = pygame.transform.scale(load_image('images_snake/apple.png'), (20, 20))
        self.food_spawn = True

        self.direction = 'RIGHT' # направление
        self.change_to = self.direction

        self.score = 0
        self.running = True
        self.drawing = True # флаг отвечающий за отрисовку начального окна
        self.run()

    def show_score(self, color, font, size):
        """Функция показывает результат"""
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.frame_size_x / 7, 40)
        self.screen.blit(score_surface, score_rect)

    def draw(self):
        """Функция рисует начальное окно"""
        self.screen.fill((113, 152, 103))
        image_snake = pygame.transform.scale(load_image('images_snake/snake.png'), (500, 550))
        self.screen.blit(image_snake, (200, 300, 100, 500))
        font = pygame.font.SysFont('impact', 80)
        text = font.render("Press any Key to Restart", True, self.dark_green)
        rect = text.get_rect(center=(450, 200))
        self.screen.blit(text, rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                # Управление кнопками
                elif event.type == pygame.KEYDOWN:
                    if self.drawing:
                        self.drawing = False
                        self.speed = 20
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

                # Проверяем условия столкновения c яблоком
                head = SnakeHead(self.head_sprites, self.snake_pos[0], self.snake_pos[1])
                if pygame.sprite.collide_mask(head, self.apple):
                    self.score += 1
                    self.food_spawn = False
                else:
                    self.snake_body.pop()  # Удаляем последний рост, если яблоко не съедено
                self.head_sprites.empty()

                # Появление яблока
                if not self.food_spawn:
                    self.food_pos = [random.randrange(110, self.frame_size_x - 200),
                                     random.randrange(110, self.frame_size_y - 200)]
                    self.apple = Food(self.food_sprites, self.food_pos)
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
            self.clock.tick(self.speed)


def play_snake():
    pygame.init()
    running = True
    size = width, height = 900, 800
    screen = pygame.display.set_mode(size)
    start_screen(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        Snake()
        pygame.display.flip()

