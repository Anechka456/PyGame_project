import pygame
import sys

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Размеры окна
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Регистрация")

# Шрифты
font = pygame.font.Font(None, 36)

# Переменные для хранения вводимых данных
username = ''
password = ''
input_box1 = pygame.Rect(100, 100, 200, 40)
input_box2 = pygame.Rect(100, 170, 200, 40)
active1 = False
active2 = False
color1 = GRAY
color2 = GRAY

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если пользователь нажал на поле ввода, активируем его
            if input_box1.collidepoint(event.pos):
                active1 = not active1
            else:
                active1 = False

            if input_box2.collidepoint(event.pos):
                active2 = not active2
            else:
                active2 = False

            # Изменяем цвет поля ввода
            color1 = (255, 0, 0) if active1 else GRAY
            color2 = (255, 0, 0) if active2 else GRAY

        if event.type == pygame.KEYDOWN:
            if active1:
                if event.key == pygame.K_RETURN:
                    print(f'Username: {username}')
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

            if active2:
                if event.key == pygame.K_RETURN:
                    print(f'Password: {password}')
                elif event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    password += event.unicode

    screen.fill(WHITE)

    # Отрисовка полей ввода
    pygame.draw.rect(screen, color1, input_box1, 2)
    pygame.draw.rect(screen, color2, input_box2, 2)

    # Отображаем текст
    txt_surface1 = font.render(username, True, BLACK)
    txt_surface2 = font.render('*' * len(password), True, BLACK)  # Скрываем пароль
    screen.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 5))
    screen.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))

    pygame.display.flip()