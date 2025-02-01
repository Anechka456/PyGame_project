import pygame
import sys

from requests import get, post, delete
from werkzeug.security import generate_password_hash, check_password_hash

server = 'https://pygameproect.pythonanywhere.com'

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
email = ''
name = pygame.Rect(WIDTH / 2 - 100, 380, 200, 40)
passwors_registr = pygame.Rect(WIDTH / 2 - 100, 450, 200, 40)
email_registr = pygame.Rect(WIDTH / 2 - 100, 520, 200, 40)
registr = pygame.Rect(WIDTH / 2, 320, 100, 36)
login = pygame.Rect(WIDTH / 2 - 100, 320, 100, 36)
active1 = False
active2 = False
active3 = False
active4 = False
active5 = False
color1 = GRAY
color2 = GRAY
color3 = GRAY
color4 = GRAY
color5 = GRAY


def proverka(password, name, email):
    try:
        password = ''.join(password.split())
        if name == '' and password == '' and email == '':
            Error('Ведите name and password and email')
        elif name == '' and password == '':
            Error('Ведите name and password')
        elif password == '' and email == '':
            Error('Ведите password and email')
        elif name == '' and email == '':
            Error('Ведите name and email')
        elif name == '':
            Error('Ведите Name')
        elif password == '':
            Error('Ведите password')
        elif email == '':
            Error('Ведите email')
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


# три фунции для проверки user
def check_email(email):
    """функция запрашиваем всех пользователей на сервере и проверяет если такой email"""
    return True if email in [i['email'] for i in get(f'{server}/api/users').json()['users']] else False


def check_name(name):
    """функция запрашиваем всех пользователей на сервере и проверяет если такое имя"""
    return True if name in [i['name'] for i in get(f'{server}/api/users').json()['users']] else False


def check_password(name, email, password):
    """функция запрашивает пользователя на сервер и проверяет пароль"""
    data = get(f'{server}/user_name?user={name}').json()
    return True if data['users']['email'] == email and check_password_hash(data['users']['hashed_password'],
                                                                           password) else False


def upload_to_server(name, password, email):
    if check_email(email) and check_name(name) and check_password(name, email, password):
        print('Ура ты зашел!!!!')
    else:
        print('не')


def add_user(name, email, password):
    if proverka(password, username, email):
        """функция добавляет пользователя на сервер"""
        if not check_name(name) and not check_email(email):
            return post(f'{server}/api/users', json={
                'name': name, 'email': email, 'hashed_password': password}).json()
        return False  # возвращает False если такое имя или email же есть


# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если пользователь нажал на поле ввода, активируем его
            if name.collidepoint(event.pos):
                active1 = not active1
            else:
                active1 = False

            if passwors_registr.collidepoint(event.pos):
                active2 = not active2
            else:
                active2 = False

            if registr.collidepoint(event.pos):
                add_user(name, email, password)
                active3 = not active3
            else:
                active3 = False

            if login.collidepoint(event.pos):
                upload_to_server(username, password, email)
                active4 = not active3
            else:
                active4 = False

            if email_registr.collidepoint(event.pos):
                active5 = not active5
            else:
                active5 = False

            # Изменяем цвет поля ввода
            color1 = (255, 0, 0) if active1 else GRAY
            color2 = (255, 0, 0) if active2 else GRAY
            color3 = (255, 0, 0) if active3 else GRAY
            color4 = (255, 0, 0) if active4 else GRAY
            color5 = (255, 0, 0) if active5 else GRAY

        if event.type == pygame.KEYDOWN:
            if active1:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 14:
                        username += event.unicode

            if active2:
                if event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    if len(password) < 14:
                        password += event.unicode

            if active5:
                if event.key == pygame.K_RETURN:
                    upload_to_server(username, password, email)
                elif event.key == pygame.K_BACKSPACE:
                    email = email[:-1]
                else:
                    if len(email) < 14:
                        email += event.unicode

    screen.fill(WHITE)

    # Отрисовка полей ввода
    pygame.draw.rect(screen, color1, name, 2)
    pygame.draw.rect(screen, color2, passwors_registr, 2)
    pygame.draw.rect(screen, color3, registr, 2)
    pygame.draw.rect(screen, color4, login, 2)
    pygame.draw.rect(screen, color5, email_registr, 2)

    # Отображаем текст
    txt_surface1 = font.render(username, True, BLACK)
    txt_surface2 = font.render(password, True, BLACK)
    txt_surface3 = font.render(email, True, BLACK)
    '''txt_surface2 = font.render('*' * len(password), True, BLACK)  # Скрывание пароля'''
    screen.blit(txt_surface1, (name.x + 5, name.y + 5))
    screen.blit(txt_surface2, (passwors_registr.x + 5, passwors_registr.y + 5))
    screen.blit(txt_surface3, (email_registr.x + 5, email_registr.y + 5))

    pygame.display.flip()
