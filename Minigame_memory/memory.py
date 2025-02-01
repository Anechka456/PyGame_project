import random
import sys

import pygame

from Minigame_memory.final_window import FinalWindowMemory
from load_image import load_image

IMAGE = None
LAST_OPEN = float('-inf')
MOVES = 12


class MemoryCard:
    def __init__(self, id_, size):
        self.id = id_
        self.image = pygame.transform.scale(load_image(f'images_memory/{id_}.jpg'), (size, size))
        self.open = False
        self.open_time = 0
        self.size = size

    def get_click(self):
        """функция открывает карточку"""
        global IMAGE, LAST_OPEN, MOVES
        if not self.open:
            if IMAGE is None:
                IMAGE = self
            elif IMAGE != self:
                self.open = True
                IMAGE.open = True
                if self.id == IMAGE.id:
                    self.open_time = float('inf')
                    IMAGE.open_time = float('inf')
                else:
                    self.open_time = pygame.time.get_ticks()
                    IMAGE.open_time = pygame.time.get_ticks()
                    LAST_OPEN = pygame.time.get_ticks()
                    MOVES -= 1
                IMAGE = None

    def update(self):
        if pygame.time.get_ticks() - self.open_time >= 600:
            self.open = False

    def draw(self, screen, x, y):
        global IMAGE
        if IMAGE == self or self.open:
            screen.blit(self.image, (x, y))
        else:
            pygame.draw.rect(screen, (39, 33, 33), pygame.Rect(x, y, self.size, self.size), width=0)
        pygame.draw.rect(screen, (72, 30, 30), pygame.Rect(x, y, self.size, self.size), width=5)


def memory(screen, n):
    global MOVES

    size2 = 700 // n
    size = int(size2 * 0.8)

    pygame.mixer.init()
    # звуки
    sound_card = pygame.mixer.Sound('data/images_memory/cards.mp3')
    sound_click = pygame.mixer.Sound('data/images/click.mp3')

    cards = []
    for i in range((n ** 2 // 2)):
        cards.extend([MemoryCard(i, size) for _ in range(2)])
    random.shuffle(cards)
    board = [[] for _ in range(n)]
    for i, card in enumerate(cards):
        board[i // n].append(card)
    font = pygame.font.SysFont('impact', 50)
    MOVES = int(n ** 2 * 0.75)

    exit_button = pygame.Rect((900 - 150, 20, 140, 50))
    text_color = (255, 204, 153)
    button_color = (255, 153, 51)
    font_button = pygame.font.SysFont('impact', 30)
    text_surface = font_button.render('Выход', True, text_color)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.time.get_ticks() - LAST_OPEN >= 600:
                # отслеживание нажатия на карточку
                mx, my = event.pos
                mx, my = mx - 110, my - 110
                x, y = mx // size2, my // size2
                if mx >= 0 and my >= 0 and x < len(board[0]) and y < len(
                        board) and mx % size2 <= size and my % size2 <= size:
                    board[y][x].get_click()
                    sound_card.play()
            if event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(event.pos):
                sound_click.play()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    running = False

        screen.fill((66, 52, 49))
        pygame.draw.rect(screen, button_color, exit_button)
        screen.blit(text_surface, (900 - 125, 25))
        screen.blit(font.render(f'Осталось попыток: {MOVES}', True, (255, 204, 153)), (40, 20))
        for i in range(len(board)):
            for j in range(len(board[i])):
                board[i][j].update()
                board[i][j].draw(screen, 110 + size2 * j, 110 + size2 * i)

        pygame.display.flip()
        clock.tick(60)

        if MOVES < 0:
            # действия если попытки закончились
            running = False
            FinalWindowMemory(n, 'К сожалению вы проиграли!')
        elif all(map(lambda x: all(map(lambda y: y.open, x)), board)):
            # действия если все карточки открыты
            running = False
            FinalWindowMemory(n, 'Вы выйграли!')
