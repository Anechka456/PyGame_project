import copy
import random

import pygame

from Minigame_minisweeper.final_window import FinalWindowSweeper
from load_image import load_image


class Sweeper:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pole = [[[] for _ in range(self.x)] for _ in range(self.y)]
        self.hidden_field = [[[] for _ in range(self.x)] for _ in range(self.y)]
        self.bomb = []
        self.number_bomb = int(self.x * self.y * 0.2)
        self.points_flag = []
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                self.bomb.append((i, j))
        self.hod = [1]

    def creating_field(self, kor):
        del self.hod[0]
        # раставляем бомбы
        del self.bomb[self.bomb.index(kor)]
        points_bomb = random.sample(self.bomb, self.number_bomb)
        for i in points_bomb:
            self.hidden_field[i[0]][i[1]] = '*'

        # создаем такой же список поля и делаем ему рамку чтобы не писать дополнительные условия
        poleframe = copy.deepcopy(self.hidden_field)
        poleframe.append([[] for _ in range(int(self.x))])
        poleframe.insert(0, [[] for _ in range(int(self.x))])
        for i in poleframe:
            i.append([])
            i.insert(0, [])

        # расставляем цифры
        for row in range(len(self.hidden_field)):
            row = row + 1
            for col in range(len(self.hidden_field[row - 1])):
                kol_bomb = 0
                col = col + 1
                if poleframe[row][col] == '*':
                    continue
                if poleframe[row][col - 1] == '*':
                    kol_bomb += 1
                if poleframe[row - 1][col - 1] == '*':
                    kol_bomb += 1
                if poleframe[row - 1][col] == '*':
                    kol_bomb += 1
                if poleframe[row - 1][col + 1] == '*':
                    kol_bomb += 1
                if poleframe[row][col + 1] == '*':
                    kol_bomb += 1
                if poleframe[row + 1][col + 1] == '*':
                    kol_bomb += 1
                if poleframe[row + 1][col] == '*':
                    kol_bomb += 1
                if poleframe[row + 1][col - 1] == '*':
                    kol_bomb += 1
                self.hidden_field[row - 1][col - 1] = kol_bomb

    def open_cell(self, coord):
        # возращаем True если клетка уже открытка
        if self.pole[coord[0]][coord[1]] != []:
            return True

        # открываем клетку если на ней не стоит флажок
        if self.pole[coord[0]][coord[1]] != 'F':
            self.pole[coord[0]][coord[1]] = self.hidden_field[coord[0]][coord[1]]
        else:
            return

        # открываем соседние клетки если клетка нулевая
        if self.pole[coord[0]][coord[1]] == 0:
            row, col = coord[0], coord[1]

            if 0 <= row < self.x and 0 <= col - 1 < self.y:
                if self.hidden_field[row][col - 1] != '*':
                    self.open_cell((row, col - 1))

            if 0 <= row - 1 < self.x and 0 <= col - 1 < self.y:
                if self.hidden_field[row - 1][col - 1] != '*':
                    self.open_cell((row - 1, col - 1))

            if 0 <= row - 1 < self.x and 0 <= col < self.y:
                if self.hidden_field[row - 1][col] != '*':
                    self.open_cell((row - 1, col))

            if 0 <= row - 1 < self.x and 0 <= col + 1 < self.y:
                if self.hidden_field[row - 1][col + 1] != '*':
                    self.open_cell((row - 1, col + 1))

            if 0 <= row < self.x and 0 <= col + 1 < self.y:
                if self.hidden_field[row][col + 1] != '*':
                    self.open_cell((row, col + 1))

            if 0 <= row + 1 < self.x and 0 <= col + 1 < self.y:
                if self.hidden_field[row + 1][col + 1] != '*':
                    self.open_cell((row + 1, col + 1))

            if 0 <= row + 1 < self.x and 0 <= col < self.y:
                if self.hidden_field[row + 1][col] != '*':
                    self.open_cell((row + 1, col))

            if 0 <= row + 1 < self.x and 0 <= col - 1 < self.y:
                if self.hidden_field[row + 1][col - 1] != '*':
                    self.open_cell((row + 1, col - 1))

    def flag_cell(self, coord):
        self.pole[coord[0]][coord[1]] = 'F'

    def open_flag_cell(self, coord):
        self.pole[coord[0]][coord[1]] = []

    def print_pole(self):
        for row in self.pole:
            st = []
            for col in row:
                if col == []:
                    st.append(col)
                    continue
                el = f"{col}"
                st.append(el.rjust(2, ' '))
            print(*st)

    def print_hidden_pole(self):
        for row in self.hidden_field:
            st = []
            for col in row:
                if col == []:
                    st.append(col)
                    continue
                el = f"{col}"
                st.append(el.rjust(2, ' '))
            print(*st)

    def display_hidden_field(self):
        for row in range(len(self.hidden_field)):
            for col in range(len(self.hidden_field[row])):
                if self.hidden_field[row][col] == '*' and self.pole[row][col] != 'F':
                    self.pole[row][col] = '*'
                    continue
                self.open_cell((row, col))

    def check_win(self):
        for row in range(self.y):
            for col in range(self.x):
                if self.hidden_field[row][col] != '*' and self.pole[row][col] == []:
                    return False
        return True

    def game_over(self):
        self.display_hidden_field()


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[-1] * width for _ in range(height)]
        self.board_hidden = [[-1] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 200
        self.top = 200
        self.cell_size = int((min(900, 800) // max(self.width, self.height)) / 1.54)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        pygame.draw.rect(self.screen, (130, 130, 130),
                         (190, 150, self.cell_size * self.width + 20, self.cell_size * self.height + 60))
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == []:
                    image = pygame.transform.scale(load_image("images_sweeper/cell.jpg"),
                                                   (self.cell_size, self.cell_size))
                elif self.board[y][x] == 'F':
                    image = pygame.transform.scale(load_image("images_sweeper/flag.jpg"),
                                                   (self.cell_size, self.cell_size))
                elif self.board[y][x] == '*':
                    image = pygame.transform.scale(load_image("images_sweeper/cell_bomb.jpg"),
                                                   (self.cell_size, self.cell_size))
                else:
                    num = self.board[y][x]
                    if num == 0:
                        image = pygame.transform.scale(load_image(f"images_sweeper/open_cell.jpg"),
                                                       (self.cell_size, self.cell_size))
                    else:
                        image = pygame.transform.scale(load_image(f"images_sweeper/cell_{num}.jpg"),
                                                       (self.cell_size, self.cell_size))
                screen.blit(image, (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size))

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[1] < self.left + self.height * self.cell_size and \
                self.top <= mouse_pos[0] < self.top + self.width * self.cell_size:
            return (int((mouse_pos[1] - self.left) / self.cell_size), int((mouse_pos[0] - self.top) / self.cell_size))
        else:
            return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            return cell
        else:
            return None


class Play(Board, Sweeper):
    def __init__(self, width, height):
        super().__init__(width, height)

        pygame.init()
        pygame.mixer.init()
        self.sound_flag = pygame.mixer.Sound('data/images_sweeper/tick.mp3')
        self.sound_win = pygame.mixer.Sound('data/images_sweeper/win.mp3')
        self.sound_lose = pygame.mixer.Sound('data/images_sweeper/lose.mp3')
        self.sound_click = pygame.mixer.Sound('data/images_sweeper/click.mp3')

        self.sweeper = Sweeper(width, height)
        self.x = width
        self.y = height
        self.size = width, height = 900, 800
        self.screen = pygame.display.set_mode((width, height))
        self.screen2 = pygame.Surface((500, 600))
        pygame.display.set_caption('Game Minisweeper')

        self.background_color = (99, 69, 48)
        self.text_color = (243, 179, 145)
        self.image_new_game = pygame.transform.scale(load_image(f"images_sweeper/emoji.jpg"),
                                                     (50, 40))
        self.exit_button = pygame.Rect((self.size[0] - 150, 20, 140, 50))
        self.new_game_button = pygame.Rect(
            (self.cell_size * self.x // 2 + 180, 155, 50, 40))

        self.dictionary_levels = {10: '1', 13: '2', 15: '3'}

        self.clock = pygame.time.Clock()
        self.timer_started = False
        self.start_ticks = None
        self.stop_time = None
        self.game_active = True
        self.fps = 60
        self.running = True
        self.play()

    def placement(self):
        for y in range(self.y):
            for x in range(self.x):
                self.board[y][x] = self.sweeper.pole[y][x]

    def double_tap_verification(self, coord):
        if self.sweeper.pole[coord[0]][coord[1]] == []:
            return False
        directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        for dx, dy in directions:
            nx, ny = coord[0] + dx, coord[1] + dy
            if 0 <= nx < self.y and 0 <= ny < self.x:
                if self.sweeper.pole[nx][ny] == 'F' and self.sweeper.hidden_field[nx][ny] == '*':
                    continue
                elif self.sweeper.pole[nx][ny] != 'F' and self.sweeper.hidden_field[nx][ny] == '*':
                    self.game_over()
                    return False
                elif self.sweeper.pole[nx][ny] == 'F' and self.sweeper.hidden_field[nx][ny] != '*':
                    return False
        return True

    def time(self):
        # отображаем время
        pygame.draw.rect(self.screen, (0, 0, 0), (200, 155, 100, 40))
        pygame.draw.rect(self.screen, (128, 128, 128), (200, 155, 100, 40), 3)
        font = pygame.font.Font('data/Crystal.ttf', 37)
        # Вычисляем прошедшее время в секундах
        if self.timer_started:
            seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000  # Превращаем в секунды
            time = str(seconds).rjust(3, '0')
        else:
            if self.stop_time:
                time = str(self.stop_time).rjust(3, '0')
            else:
                time = '000'
        text = font.render(time, True, (255, 0, 0))
        self.screen.blit(text, (200 + 25, 155))

        # отбражаем количество бомб
        pygame.draw.rect(self.screen, (0, 0, 0), (self.cell_size * self.x + 100, 155, 100, 40))
        pygame.draw.rect(self.screen, (128, 128, 128), (self.cell_size * self.x + 100, 155, 100, 40), 3)
        font = pygame.font.Font('data/Crystal.ttf', 37)
        bombs = str(self.sweeper.number_bomb).rjust(3, '0')
        text = font.render(bombs, True, (255, 0, 0))
        self.screen.blit(text, (self.cell_size * self.x + 125, 155))

    def new_game(self):
        self.timer_started = False
        self.start_ticks = None
        self.image_new_game = pygame.transform.scale(load_image(f"images_sweeper/emoji.jpg"),
                                                     (50, 40))
        self.sweeper = Sweeper(self.x, self.y)
        self.game_active = True

    def game_over(self):
        self.sound_lose.play()
        self.sweeper.game_over()
        self.timer_started = False
        self.stop_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.image_new_game = pygame.transform.scale(
            load_image(f"images_sweeper/emoji_died.jpg"),
            (50, 40))
        self.game_active = False
        FinalWindowSweeper(1, self.dictionary_levels[self.x], self.stop_time)

    def game_win(self):
        self.sound_win.play()
        self.timer_started = False
        self.stop_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.game_active = False
        FinalWindowSweeper(2, self.dictionary_levels[self.x], self.stop_time)

    def draw_button(self):
        self.screen.blit(self.image_new_game, self.new_game_button)

        font = pygame.font.SysFont('impact', 30)
        pygame.draw.rect(self.screen, (168, 101, 64), self.exit_button)
        text_surface = font.render('Выход', True, self.text_color)
        self.screen.blit(text_surface, (self.size[0] - 125, 25))

    def double_tap(self, coord):
        if self.game_active:
            if self.double_tap_verification(coord):
                directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
                for dx, dy in directions:
                    nx, ny = coord[0] + dx, coord[1] + dy
                    if 0 <= nx < self.y and 0 <= ny < self.x:
                        self.sweeper.open_cell((nx, ny))
                if self.sweeper.check_win():
                    self.game_win()

    def clicking_left(self, coord):
        if self.game_active:
            if self.sweeper.hod:
                self.sweeper.creating_field((coord[0], coord[1]))
                self.timer_started = True
                self.start_ticks = pygame.time.get_ticks()  # Получаем текущее время в миллисекундах
            if self.sweeper.pole[coord[0]][coord[1]] != 'F':
                self.sound_click.play()
                if self.sweeper.hidden_field[coord[0]][coord[1]] != '*':
                    self.sweeper.open_cell((coord[0], coord[1]))
                else:
                    self.game_over()
            if self.game_active:
                if self.sweeper.check_win():
                    self.game_win()

    def clicking_right(self, coord):
        if self.game_active:
            if (coord[0], coord[1]) in self.sweeper.points_flag:
                self.sweeper.number_bomb += 1
                del self.sweeper.points_flag[self.sweeper.points_flag.index((coord[0], coord[1]))]
                self.sweeper.open_flag_cell((coord[0], coord[1]))
            else:
                if self.sweeper.pole[coord[0]][coord[1]] == []:
                    self.sound_flag.play()
                    self.sweeper.number_bomb -= 1
                    self.sweeper.points_flag.append((coord[0], coord[1]))
                    self.sweeper.flag_cell((coord[0], coord[1]))

    def play(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = pygame.mouse.get_pressed()
                    mouse_pos = event.pos
                    if (mouse_pressed[0] and mouse_pressed[2]) or mouse_pressed[1]:
                        coord = self.get_click(event.pos)
                        if coord:
                            self.double_tap(coord)

                    elif event.button == 1:
                        coord = self.get_click(event.pos)
                        if coord:
                            self.clicking_left(coord)
                        elif self.exit_button.collidepoint(mouse_pos):
                            self.running = False
                        elif self.new_game_button.collidepoint(mouse_pos):
                            self.new_game()

                    elif event.button == 3:
                        coord = self.get_click(event.pos)
                        if coord:
                            self.clicking_right(coord)

            self.placement()
            self.screen.fill(self.background_color)
            self.render(self.screen)
            self.draw_button()
            self.time()
            self.clock.tick(self.fps)
            pygame.display.flip()
