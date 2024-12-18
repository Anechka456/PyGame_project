import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
FPS_CLOCK = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventures with mini")

# Персонаж
character_image = pygame.image.load('images/character.jpg')
character_rect = character_image.get_rect()
character_image = pygame.transform.scale(character_image, (60, 60))
player_size = 60
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 4

# Интерактивные точки
interactive_points = [[100, 150], [300, 400], [500, 200], [700, 350]]


# Функция для создания нового окна с мини игрой
def open_new_game_window():
    new_game = pygame.Surface((300, 300))
    new_game.fill(WHITE)

    # Игровой цикл новой игры
    new_game_running = True
    while new_game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                new_game_running = False

        screen.fill(WHITE)
        screen.blit(new_game, (250, 150))
        pygame.display.flip()
        FPS_CLOCK.tick(FPS)


# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Проверка на столкновение с интерактивными точками
    for point in interactive_points:
        if (player_pos[0] < point[0] < player_pos[0] + player_size) and \
                (player_pos[1] < point[1] < player_pos[1] + player_size):
            player_pos = [WIDTH // 2, HEIGHT // 2]
            open_new_game_window()

    # Отрисовка
    screen.fill(BLACK)
    screen.blit(character_image, (player_pos[0], player_pos[1], player_size, player_size))

    # Отрисовка интерактивных точек
    for point in interactive_points:
        pygame.draw.circle(screen, RED, point, 10)

    pygame.display.flip()
    FPS_CLOCK.tick(FPS)

pygame.quit()
sys.exit()
