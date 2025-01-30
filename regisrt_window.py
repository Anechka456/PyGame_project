import pygame
import sys

# Инициализация Pygame
pygame.init()

proverka_abs = ['qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop', 'asd', 'sdf', 'dfg',
                'fgh', 'ghj', 'hjk', 'jkl', 'zxc', 'xcv', 'cvb', 'vbn', 'bnm', 'йцу', 'цук',
                'уке', 'кен',
                'енг', 'нгш', 'гшщ', 'шщз', 'щзх', 'зхъ', 'фыв', 'ыва', 'вап', 'апр', 'про',
                'рол', 'олд',
                'лдж', 'джэ', 'ячс', 'чсм', 'сми', 'мит', 'ить', 'тьб', 'ьбю', 'жэё']
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Размеры окна
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Регистрация")

# Шрифты
font = pygame.font.Font(None, 36)

# Переменные для хранения вводимых данных
username = ''
password = ''
input_box1 = pygame.Rect(WIDTH / 2 - 100, 100, 200, 40)
input_box2 = pygame.Rect(WIDTH / 2 - 100, 170, 200, 40)
login = pygame.Rect(50, 50, 50, 50)
active1 = False
active2 = False
active3 = False
color1 = GRAY
color2 = GRAY
color3 = GRAY


def proverka(password, name):
    try:
        password = ''.join(password.split())
        if name == '' and password == '':
            Error('Ведите Name and password')
        elif name == '':
            Error('Ведите Name')
        elif password == '':
            Error('Ведите password')
        elif len(password) < 4:
            raise ValueError
        elif password.isdigit():
            raise ValueError
        elif password.isalpha():
            raise ValueError
        elif password.islower():
            raise ValueError
        elif password.isupper():
            raise ValueError
        for i in proverka_abs:
            if i in password.lower():
                raise ValueError
        flag_number = False
        flag_lower = False
        flag_upper = False
        for letter in password:
            if letter.isdigit():
                flag_number = True
            if letter.isupper():
                flag_upper = True
            if letter.islower():
                flag_lower = True
        if flag_lower and flag_upper and flag_number:
            return True
    except Exception:
        Error('Неверный пороль')


def Error(text):
    print(text)  # Создвние менюшки ошибки


def Login(active1, active2):
    if proverka(password, username):
        print('занесение в б д')



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

            if login.collidepoint(event.pos):
                Login(active1, active2)
                active3 = not active3
            else:
                active3 = False

            # Изменяем цвет поля ввода
            color1 = (255, 0, 0) if active1 else GRAY
            color2 = (255, 0, 0) if active2 else GRAY
            color3 = (255, 0, 0) if active3 else GRAY

        if event.type == pygame.KEYDOWN:
            if active1:
                if event.key == pygame.K_RETURN:
                    Login(active1, active2)
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 14:
                        username += event.unicode

            if active2:
                if event.key == pygame.K_RETURN:
                    Login(active1, active2)
                elif event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    if len(password) < 14:
                        password += event.unicode

    screen.fill(WHITE)

    # Отрисовка полей ввода
    pygame.draw.rect(screen, color1, input_box1, 2)
    pygame.draw.rect(screen, color2, input_box2, 2)
    pygame.draw.rect(screen, color3, login, 2)

    # Отображаем текст
    txt_surface1 = font.render(username, True, BLACK)
    txt_surface2 = font.render(password, True, BLACK)
    '''txt_surface2 = font.render('*' * len(password), True, BLACK)  # Скрывание пароля'''
    screen.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 5))
    screen.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))

    pygame.display.flip()
